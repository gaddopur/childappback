import json
import logging
import random
import os
import time
from pathlib import Path
from threading import Lock

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIKeyManager:
    def __init__(self, api_keys=None):  # Correct parameter name
        self.lock = Lock()
        self.keys_file = Path("api_keys.json")
        self.state_file = Path("api_key_states.json")
        self.key_states = {}
        
        # Correct variable name usage
        self.api_keys = api_keys if api_keys is not None else self._load_keys()
        self._validate_keys()
        self.load_states()

    def _validate_keys(self):
        """Validate we have at least one API key"""
        if not self.api_keys:
            raise ValueError("No API keys provided or found in environment variables")
        logging.info(f"Initialized with {len(self.api_keys)} API keys")

    def _load_keys(self):
        """Load API keys from storage file"""
        try:
            if self.keys_file.exists():
                with open(self.keys_file, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            logging.error(f"Error loading keys: {e}")
            return []

    def _save_keys(self):
        """Save API keys to file"""
        try:
            with open(self.keys_file, "w") as f:
                json.dump(self.api_keys, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Error saving keys: {e}")
            return False

    def load_states(self):
        """Load persisted key states from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file, "r") as f:
                    self.key_states = json.load(f)
        except Exception as e:
            logging.error(f"Error loading states: {e}")

    def save_states(self):
        """Persist current key states to file"""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.key_states, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving states: {e}")

    def get_available_key(self):
        """Get a random available API key"""
        with self.lock:
            now = time.time()
            available = [
                key for key in self.api_keys
                if self.key_states.get(key, {}).get("blocked_until", 0) < now
            ]
            return random.choice(available) if available else None

    def update_key_status(self, key, success):
        """Update key status based on usage outcome"""
        with self.lock:
            if success:
                if key in self.key_states:
                    del self.key_states[key]
                    self.save_states()
            else:
                now = time.time()
                failures = self.key_states.get(key, {}).get("failures", 0) + 1
                backoff = min(3600, 300 * (2 ** failures))
                self.key_states[key] = {
                    "blocked_until": now + backoff,
                    "failures": failures,
                    "last_failed": now
                }
                self.save_states()

    def get_key_status(self, key):
        """Get current status of a specific key"""
        status = self.key_states.get(key, {})
        return {
            "blocked_until": status.get("blocked_until", 0),
            "failures": status.get("failures", 0),
            "last_failed": status.get("last_failed", 0)
        }
    
    def get_all_keys(self):
        """Get a copy of all API keys in a thread-safe manner"""
        with self.lock:
            return self.api_keys.copy()