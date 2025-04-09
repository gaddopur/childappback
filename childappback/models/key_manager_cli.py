import json
import getpass
from pathlib import Path
from api_key_manager import APIKeyManager
import time

def show_menu():
    print("\nAPI Key Management Console")
    print("1. Add new API Key")
    print("2. List stored API Keys")
    print("3. Remove API Key")
    print("4. View Key Statuses")
    print("5. Exit")
    return input("Enter your choice (1-5): ").strip()

def add_key(manager):
    key = getpass.getpass("Enter API key (input hidden): ").strip()
    if not key:
        print("Error: Key cannot be empty!")
        return
    
    if key in manager.api_keys:
        print("Error: Key already exists!")
        return
    
    manager.api_keys.append(key)
    if manager._save_keys():
        print(f"Key added successfully! (Partial: {key[:4]}...{key[-4:]})")
    else:
        print("Failed to save key to storage!")
        manager.api_keys.pop()

def list_keys(manager):
    if not manager.api_keys:
        print("No API keys stored")
        return
    
    print("\nStored API Keys:")
    for idx, key in enumerate(manager.api_keys, 1):
        status = manager.get_key_status(key)
        state = "Active" if status['blocked_until'] < time.time() else "Blocked"
        print(f"{idx}. {key[:4]}...{key[-4:]} ({state})")

def remove_key(manager):
    list_keys(manager)
    if not manager.api_keys:
        return
    
    try:
        choice = int(input("Enter key number to remove: "))
        if 1 <= choice <= len(manager.api_keys):
            removed_key = manager.api_keys.pop(choice-1)
            if manager._save_keys():
                print(f"Removed key: ...{removed_key[-4:]}")
            else:
                print("Failed to save changes!")
                manager.api_keys.insert(choice-1, removed_key)
        else:
            print("Invalid selection")
    except ValueError:
        print("Please enter a valid number")

def view_statuses(manager):
    print("\nKey Status Overview:")
    for key in manager.api_keys:
        status = manager.get_key_status(key)
        print(f"Key {key[:4]}...{key[-4:]}:")
        print(f"  Failures: {status['failures']}")
        print(f"  Blocked until: {time.ctime(status['blocked_until'])}")
        print(f"  Last failed: {time.ctime(status['last_failed']) if status['last_failed'] else 'Never'}")
        print()

def main():
    manager = APIKeyManager()
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            add_key(manager)
        elif choice == '2':
            list_keys(manager)
        elif choice == '3':
            remove_key(manager)
        elif choice == '4':
            view_statuses(manager)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()