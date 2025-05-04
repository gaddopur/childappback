import json
import logging
import random
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from childappback.settings import BASE_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIKeyManager:
    def __init__(self, api_keys=None):
        self.lock = Lock()
        self.keys_file = BASE_DIR / Path("models") / "api_keys.json"
        self.state_file = BASE_DIR / Path("models") / "api_key_states.json"
        self.key_states = {}
        
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
                    content = f.read()
                    if content.strip():  # Check if file is not empty
                        states = json.loads(content)
                        self.key_states = {
                            key: {
                                "blocked_until": datetime.fromisoformat(state["blocked_until"]),
                                "failures": state["failures"],
                                "last_failed": datetime.fromisoformat(state["last_failed"]) if state.get("last_failed") else None
                            } for key, state in states.items()
                        }
        except Exception as e:
            logging.error(f"Error loading states: {e}")

    def save_states(self):
        """Persist current key states to file"""
        try:
            with open(self.state_file, "w") as f:
                json.dump({
                    key: {
                        "blocked_until": state["blocked_until"].isoformat(),
                        "failures": state["failures"],
                        "last_failed": state["last_failed"].isoformat() if state["last_failed"] else None
                    } for key, state in self.key_states.items()
                }, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving states: {e}")


    def get_available_key(self):
        """Get a random available API key"""
        with self.lock:
            now = datetime.now()
            available = [
                key for key in self.api_keys
                if self.key_states.get(key, {}).get("blocked_until", datetime.min) < now
            ]
            return random.choice(available) if available else None

    def update_key_status(self, key, success):
        """Update key status based on usage outcome"""
        with self.lock:
            now = datetime.now()
            if success:
                # Add a 6-second cooldown after successful usage
                self.key_states[key] = {
                    "blocked_until": now + timedelta(seconds=6),
                    "failures": 0,
                    "last_failed": None
                }
                self.save_states()
            else:
                # Block the key for 6 hours upon failure
                backoff = timedelta(hours=6)
                self.key_states[key] = {
                    "blocked_until": now + backoff,
                    "failures": self.key_states.get(key, {}).get("failures", 0) + 1,
                    "last_failed": now
                }
                self.save_states()


    def get_key_status(self, key):
        """Get current status of a specific key"""
        status = self.key_states.get(key, {})
        return {
            "blocked_until": status.get("blocked_until", datetime.min),
            "failures": status.get("failures", 0),
            "last_failed": status.get("last_failed", datetime.min)
        }
    
    def get_all_keys(self):
        """Get a copy of all API keys in a thread-safe manner"""
        with self.lock:
            return self.api_keys.copy()
