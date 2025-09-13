#!/usr/bin/env python3
"""
WiFi Password Manager - A simple utility to manage WiFi passwords.
"""

import re
import hashlib
from typing import Dict, List, Optional


class WiFiPasswordManager:
    """A simple WiFi password manager for storing and retrieving WiFi credentials."""
    
    def __init__(self):
        self.passwords: Dict[str, str] = {}
        self.encrypted_passwords: Dict[str, str] = {}
    
    def add_password(self, ssid: str, password: str) -> bool:
        """
        Add a WiFi password for a given SSID.
        
        Args:
            ssid: The network SSID (name)
            password: The WiFi password
            
        Returns:
            True if password was added successfully, False otherwise
        """
        if not self.validate_ssid(ssid):
            return False
        
        if not self.validate_password(password):
            return False
        
        self.passwords[ssid] = password
        self.encrypted_passwords[ssid] = self._encrypt_password(password)
        return True
    
    def get_password(self, ssid: str) -> Optional[str]:
        """
        Retrieve the password for a given SSID.
        
        Args:
            ssid: The network SSID
            
        Returns:
            The password if found, None otherwise
        """
        return self.passwords.get(ssid)
    
    def remove_password(self, ssid: str) -> bool:
        """
        Remove a stored password for a given SSID.
        
        Args:
            ssid: The network SSID
            
        Returns:
            True if password was removed, False if SSID not found
        """
        if ssid in self.passwords:
            del self.passwords[ssid]
            if ssid in self.encrypted_passwords:
                del self.encrypted_passwords[ssid]
            return True
        return False
    
    def list_networks(self) -> List[str]:
        """
        Get a list of all stored network SSIDs.
        
        Returns:
            List of SSID strings
        """
        return list(self.passwords.keys())
    
    def validate_ssid(self, ssid: str) -> bool:
        """
        Validate an SSID according to WiFi standards.
        
        Args:
            ssid: The SSID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not ssid or not isinstance(ssid, str):
            return False
        
        # SSID must be 1-32 characters
        if len(ssid) < 1 or len(ssid) > 32:
            return False
        
        # SSID cannot be only whitespace
        if ssid.isspace():
            return False
        
        return True
    
    def validate_password(self, password: str) -> bool:
        """
        Validate a WiFi password according to WPA/WPA2 standards.
        
        Args:
            password: The password to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not password or not isinstance(password, str):
            return False
        
        # WPA/WPA2 passwords must be 8-63 characters
        if len(password) < 8 or len(password) > 63:
            return False
        
        return True
    
    def _encrypt_password(self, password: str) -> str:
        """
        Simple password encryption using SHA-256.
        
        Args:
            password: The password to encrypt
            
        Returns:
            Encrypted password hash
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, ssid: str, password: str) -> bool:
        """
        Verify if the provided password matches the stored password for an SSID.
        
        Args:
            ssid: The network SSID
            password: The password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        if ssid not in self.encrypted_passwords:
            return False
        
        encrypted_input = self._encrypt_password(password)
        return encrypted_input == self.encrypted_passwords[ssid]
    
    def clear_all(self) -> None:
        """Clear all stored passwords."""
        self.passwords.clear()
        self.encrypted_passwords.clear()
    
    def count(self) -> int:
        """
        Get the number of stored networks.
        
        Returns:
            Number of stored networks
        """
        return len(self.passwords)


def main():
    """Simple CLI interface for the WiFi Password Manager."""
    manager = WiFiPasswordManager()
    
    print("WiFi Password Manager")
    print("Commands: add, get, remove, list, quit")
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command == "quit" or command == "exit":
            break
        elif command == "add":
            ssid = input("Enter SSID: ").strip()
            password = input("Enter password: ").strip()
            if manager.add_password(ssid, password):
                print(f"Password added for {ssid}")
            else:
                print("Failed to add password. Check SSID and password validity.")
        elif command == "get":
            ssid = input("Enter SSID: ").strip()
            password = manager.get_password(ssid)
            if password:
                print(f"Password for {ssid}: {password}")
            else:
                print(f"No password found for {ssid}")
        elif command == "remove":
            ssid = input("Enter SSID: ").strip()
            if manager.remove_password(ssid):
                print(f"Password removed for {ssid}")
            else:
                print(f"No password found for {ssid}")
        elif command == "list":
            networks = manager.list_networks()
            if networks:
                print("Stored networks:")
                for network in networks:
                    print(f"  - {network}")
            else:
                print("No networks stored")
        else:
            print("Unknown command. Available: add, get, remove, list, quit")


if __name__ == "__main__":
    main()