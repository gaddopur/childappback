import json
import logging
import random
import os
import time
import hashlib
from threading import Lock

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class APIKeyManager:
    def __init__(self, api_keys=None, persistence_file='key_statuses.json'):
        self.lock = Lock()
        self.persistence_file = persistence_file
        
        # Load keys from parameter or environment
        self.api_keys = api_keys if api_keys is not None else self._load_keys()
        self._validate_keys()
        
        # Load persisted states after keys are validated
        self.key_states = self._load_persisted_states()

    def _hash_key(self, key: str) -> str:
        """Generate SHA-256 hash for key identification"""
        return hashlib.sha256(key.encode()).hexdigest()

    def _validate_keys(self):
        """Validate we have at least one API key"""
        if not self.api_keys:
            raise ValueError("No API keys provided in constructor or API_KEYS environment variable")
        logging.info(f"Initialized with {len(self.api_keys)} API keys")

    def _load_keys(self):
        """Load API keys from environment variable"""
        keys_str = os.environ.get("API_KEYS", "")
        if not keys_str:
            return []
        
        keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        return list(set(keys))  # Remove duplicates

    def _load_persisted_states(self):
        """Load persisted states from JSON file, filtering out non-existent keys"""
        if not os.path.exists(self.persistence_file):
            return {}
        
        try:
            with open(self.persistence_file, 'r') as f:
                persisted = json.load(f)
            
            # Filter out entries for keys that no longer exist
            current_hashes = {self._hash_key(k) for k in self.api_keys}
            return {k: v for k, v in persisted.items() if k in current_hashes}
        except Exception as e:
            logging.error(f"Error loading persisted states: {e}")
            return {}

    def _persist_states(self):
        """Save current states to JSON file"""
        try:
            with open(self.persistence_file, 'w') as f:
                json.dump(self.key_states, f, indent=2)
        except Exception as e:
            logging.error(f"Error persisting states: {e}")

    def _is_key_available(self, key: str, current_time: float) -> bool:
        """Check if a key is available based on cooldowns"""
        hashed_key = self._hash_key(key)
        state = self.key_states.get(hashed_key, {})
        
        # Check regular 6-second cooldown
        last_used_cooldown = state.get('last_used', 0) + 6 <= current_time
        
        # Check error cooldown (6 hours)
        error_cooldown = state.get('cooldown_until', 0) <= current_time
        
        return last_used_cooldown and error_cooldown

    def get_available_key(self):
        """Get a random available API key considering both cooldowns"""
        with self.lock:
            now = time.time()
            available = [k for k in self.api_keys if self._is_key_available(k, now)]
            
            if available:
                chosen_key = random.choice(available)
                hashed_key = self._hash_key(chosen_key)
                
                # Update last_used time
                self.key_states[hashed_key] = {
                    **self.key_states.get(hashed_key, {}),
                    'last_used': now
                }
                self._persist_states()
                logging.info(f"Selected key {hashed_key} (last used at {now})")
                return chosen_key
            else:
                logging.warning("No API keys available due to cooldown")
                return None

    def update_key_status(self, key: str, success: bool, error_message: str = None, error_code: int = None):
        """Update key status and handle error cooldowns"""
        if not success and (error_message is None or error_code is None):
            raise ValueError("error_message and error_code are required when success=False")
        
        with self.lock:
            hashed_key = self._hash_key(key)
            now = time.time()
            
            if success:
                # Clear error state on successful use
                if hashed_key in self.key_states:
                    self.key_states[hashed_key].pop('cooldown_until', None)
                    self.key_states[hashed_key].pop('error_message', None)
                    self.key_states[hashed_key].pop('error_code', None)
                logging.info(f"Key {hashed_key} used successfully")
            else:
                # Set 6-hour cooldown and store error details
                cooldown_until = now + 6 * 3600  # 6 hours
                self.key_states[hashed_key] = {
                    **self.key_states.get(hashed_key, {}),
                    'cooldown_until': cooldown_until,
                    'error_message': error_message,
                    'error_code': error_code
                }
                logging.error(
                    f"Key {hashed_key} failed at {now}. "
                    f"Cooldown until {time.ctime(cooldown_until)}. "
                    f"Error {error_code}: {error_message}"
                )
            
            self._persist_states()

    def get_key_status(self, key: str) -> dict:
        """Get detailed status of a specific key"""
        hashed_key = self._hash_key(key)
        return self.key_states.get(hashed_key, {}).copy()

    def get_all_keys(self):
        """Get a copy of all API keys"""
        with self.lock:
            return self.api_keys.copy()