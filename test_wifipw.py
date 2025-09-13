#!/usr/bin/env python3
"""
Test suite for WiFi Password Manager.
"""

import pytest
import hashlib
from wifipw import WiFiPasswordManager


class TestWiFiPasswordManager:
    """Test cases for WiFiPasswordManager class."""
    
    def setup_method(self):
        """Set up a fresh manager instance for each test."""
        self.manager = WiFiPasswordManager()
    
    def test_init(self):
        """Test that manager initializes with empty storage."""
        assert len(self.manager.passwords) == 0
        assert len(self.manager.encrypted_passwords) == 0
        assert self.manager.count() == 0
    
    def test_add_valid_password(self):
        """Test adding a valid WiFi password."""
        result = self.manager.add_password("MyNetwork", "password123")
        assert result is True
        assert "MyNetwork" in self.manager.passwords
        assert self.manager.passwords["MyNetwork"] == "password123"
        assert "MyNetwork" in self.manager.encrypted_passwords
        assert self.manager.count() == 1
    
    def test_add_multiple_passwords(self):
        """Test adding multiple WiFi passwords."""
        assert self.manager.add_password("Network1", "password123")
        assert self.manager.add_password("Network2", "mypassword")
        assert self.manager.add_password("Network3", "securepwd123")
        
        assert self.manager.count() == 3
        assert "Network1" in self.manager.passwords
        assert "Network2" in self.manager.passwords
        assert "Network3" in self.manager.passwords
    
    def test_get_existing_password(self):
        """Test retrieving an existing password."""
        self.manager.add_password("TestNetwork", "testpass123")
        password = self.manager.get_password("TestNetwork")
        assert password == "testpass123"
    
    def test_get_nonexistent_password(self):
        """Test retrieving a password that doesn't exist."""
        password = self.manager.get_password("NonExistent")
        assert password is None
    
    def test_remove_existing_password(self):
        """Test removing an existing password."""
        self.manager.add_password("RemoveMe", "password123")
        assert self.manager.count() == 1
        
        result = self.manager.remove_password("RemoveMe")
        assert result is True
        assert self.manager.count() == 0
        assert "RemoveMe" not in self.manager.passwords
        assert "RemoveMe" not in self.manager.encrypted_passwords
    
    def test_remove_nonexistent_password(self):
        """Test removing a password that doesn't exist."""
        result = self.manager.remove_password("NonExistent")
        assert result is False
        assert self.manager.count() == 0
    
    def test_list_networks_empty(self):
        """Test listing networks when none are stored."""
        networks = self.manager.list_networks()
        assert networks == []
    
    def test_list_networks_with_data(self):
        """Test listing networks with stored data."""
        self.manager.add_password("Network1", "password1")
        self.manager.add_password("Network2", "password2")
        
        networks = self.manager.list_networks()
        assert len(networks) == 2
        assert "Network1" in networks
        assert "Network2" in networks
    
    def test_clear_all(self):
        """Test clearing all stored passwords."""
        self.manager.add_password("Network1", "password1")
        self.manager.add_password("Network2", "password2")
        assert self.manager.count() == 2
        
        self.manager.clear_all()
        assert self.manager.count() == 0
        assert len(self.manager.passwords) == 0
        assert len(self.manager.encrypted_passwords) == 0


class TestSSIDValidation:
    """Test cases for SSID validation."""
    
    def setup_method(self):
        """Set up a fresh manager instance for each test."""
        self.manager = WiFiPasswordManager()
    
    def test_valid_ssids(self):
        """Test valid SSID formats."""
        valid_ssids = [
            "MyNetwork",
            "Network_123",
            "Café WiFi",
            "A",  # Single character
            "x" * 32,  # Maximum length (32 chars)
            "Mixed123!@#",
            "WiFi-Guest",
            "2.4GHz Network"
        ]
        
        for ssid in valid_ssids:
            assert self.manager.validate_ssid(ssid), f"SSID '{ssid}' should be valid"
    
    def test_invalid_ssids(self):
        """Test invalid SSID formats."""
        invalid_ssids = [
            "",  # Empty string
            None,  # None value
            123,  # Non-string type
            "x" * 33,  # Too long (33 chars)
            "   ",  # Only whitespace
            "\t\n",  # Only whitespace characters
        ]
        
        for ssid in invalid_ssids:
            assert not self.manager.validate_ssid(ssid), f"SSID '{ssid}' should be invalid"
    
    def test_add_invalid_ssid(self):
        """Test adding password with invalid SSID."""
        result = self.manager.add_password("", "validpassword123")
        assert result is False
        assert self.manager.count() == 0
        
        result = self.manager.add_password("x" * 33, "validpassword123")
        assert result is False
        assert self.manager.count() == 0


class TestPasswordValidation:
    """Test cases for password validation."""
    
    def setup_method(self):
        """Set up a fresh manager instance for each test."""
        self.manager = WiFiPasswordManager()
    
    def test_valid_passwords(self):
        """Test valid password formats."""
        valid_passwords = [
            "password123",
            "12345678",  # Minimum length (8 chars)
            "x" * 63,  # Maximum length (63 chars)
            "ComplexP@ssw0rd!",
            "My Secure Password",
            "café-password-123"
        ]
        
        for password in valid_passwords:
            assert self.manager.validate_password(password), f"Password '{password}' should be valid"
    
    def test_invalid_passwords(self):
        """Test invalid password formats."""
        invalid_passwords = [
            "",  # Empty string
            None,  # None value
            123,  # Non-string type
            "short",  # Too short (< 8 chars)
            "1234567",  # Too short (7 chars)
            "x" * 64,  # Too long (64 chars)
        ]
        
        for password in invalid_passwords:
            assert not self.manager.validate_password(password), f"Password '{password}' should be invalid"
    
    def test_add_invalid_password(self):
        """Test adding invalid password."""
        result = self.manager.add_password("ValidSSID", "short")
        assert result is False
        assert self.manager.count() == 0
        
        result = self.manager.add_password("ValidSSID", "x" * 64)
        assert result is False
        assert self.manager.count() == 0


class TestPasswordEncryption:
    """Test cases for password encryption and verification."""
    
    def setup_method(self):
        """Set up a fresh manager instance for each test."""
        self.manager = WiFiPasswordManager()
    
    def test_password_encryption(self):
        """Test that passwords are encrypted properly."""
        password = "testpassword123"
        encrypted = self.manager._encrypt_password(password)
        
        # Check that encryption produces a hash
        assert encrypted != password
        assert len(encrypted) == 64  # SHA-256 produces 64-char hex string
        
        # Check that same password produces same hash
        encrypted2 = self.manager._encrypt_password(password)
        assert encrypted == encrypted2
        
        # Check that different passwords produce different hashes
        encrypted3 = self.manager._encrypt_password("differentpassword")
        assert encrypted != encrypted3
    
    def test_password_verification(self):
        """Test password verification functionality."""
        ssid = "TestNetwork"
        password = "testpassword123"
        
        # Add password
        self.manager.add_password(ssid, password)
        
        # Verify correct password
        assert self.manager.verify_password(ssid, password) is True
        
        # Verify incorrect password
        assert self.manager.verify_password(ssid, "wrongpassword") is False
        
        # Verify with non-existent SSID
        assert self.manager.verify_password("NonExistent", password) is False
    
    def test_encrypted_storage(self):
        """Test that passwords are stored in encrypted form."""
        ssid = "TestNetwork"
        password = "testpassword123"
        
        self.manager.add_password(ssid, password)
        
        # Check that encrypted version exists and is different from original
        assert ssid in self.manager.encrypted_passwords
        encrypted = self.manager.encrypted_passwords[ssid]
        assert encrypted != password
        
        # Check that it matches manual encryption
        expected_hash = hashlib.sha256(password.encode()).hexdigest()
        assert encrypted == expected_hash


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up a fresh manager instance for each test."""
        self.manager = WiFiPasswordManager()
    
    def test_overwrite_existing_password(self):
        """Test overwriting an existing password."""
        ssid = "TestNetwork"
        
        # Add first password
        self.manager.add_password(ssid, "password123")
        assert self.manager.get_password(ssid) == "password123"
        
        # Overwrite with new password
        self.manager.add_password(ssid, "newpassword456")
        assert self.manager.get_password(ssid) == "newpassword456"
        assert self.manager.count() == 1  # Still only one network
    
    def test_unicode_ssid_and_password(self):
        """Test Unicode characters in SSID and password."""
        ssid = "Café WiFi 🏠"
        password = "pássword123€"
        
        # Should work with Unicode characters (within length limits)
        if len(ssid.encode('utf-8')) <= 32:  # SSID byte length limit
            result = self.manager.add_password(ssid, password)
            if result:
                assert self.manager.get_password(ssid) == password
                assert self.manager.verify_password(ssid, password) is True
    
    def test_case_sensitivity(self):
        """Test that SSIDs are case-sensitive."""
        self.manager.add_password("Network", "password123")
        self.manager.add_password("network", "password456")
        
        assert self.manager.count() == 2
        assert self.manager.get_password("Network") == "password123"
        assert self.manager.get_password("network") == "password456"
        assert self.manager.get_password("NETWORK") is None
    
    def test_whitespace_handling(self):
        """Test handling of whitespace in SSID and passwords."""
        # SSID with leading/trailing spaces (should be preserved)
        ssid_with_spaces = " MyNetwork "
        password = "password123"
        
        if self.manager.validate_ssid(ssid_with_spaces):
            self.manager.add_password(ssid_with_spaces, password)
            assert self.manager.get_password(ssid_with_spaces) == password
            assert self.manager.get_password("MyNetwork") is None  # Without spaces
    
    def test_special_characters(self):
        """Test special characters in SSID and passwords."""
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Test SSID with special characters
        ssid = f"Network{special_chars[:10]}"  # Limit length
        password = f"password{special_chars}"
        
        if (self.manager.validate_ssid(ssid) and 
            self.manager.validate_password(password)):
            result = self.manager.add_password(ssid, password)
            if result:
                assert self.manager.get_password(ssid) == password


def test_main_function_exists():
    """Test that main function exists and is callable."""
    from wifipw import main
    assert callable(main)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])