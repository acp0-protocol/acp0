"""Test cases for crypto module"""

import pytest
import time
from acp0.core.crypto import KeyPair


def test_keypair_generation():
    """Test KeyPair generation and basic operations"""
    keypair = KeyPair()
    
    # Test public key generation
    public_key = keypair.get_public_key_base64()
    assert public_key is not None
    assert len(public_key) > 0
    
    # Test private key generation
    private_key = keypair.get_private_key_base64()
    assert private_key is not None
    assert len(private_key) > 0


def test_signature_repeatability():
    """Test 1000 signatures to ensure repeatability"""
    keypair = KeyPair()
    message = b"test message"
    
    signatures = [keypair.sign_bytes(message) for _ in range(1000)]
    
    # All signatures should be different (due to randomness)
    assert len(set(signatures)) == 1000
    
    # But all should verify correctly
    for sig in signatures:
        assert KeyPair.verify_bytes(
            message, sig, keypair.get_public_key_base64()
        )


def test_signature_verification():
    """Test signature verification with valid and invalid signatures"""
    keypair = KeyPair()
    message = b"test message"
    
    # Valid signature
    signature = keypair.sign_bytes(message)
    assert KeyPair.verify_bytes(message, signature, keypair.get_public_key_base64())
    
    # Invalid signature (wrong message)
    wrong_message = b"wrong message"
    assert not KeyPair.verify_bytes(wrong_message, signature, keypair.get_public_key_base64())
    
    # Invalid signature (wrong public key)
    wrong_keypair = KeyPair()
    assert not KeyPair.verify_bytes(message, signature, wrong_keypair.get_public_key_base64())
    
    # Invalid signature (malformed signature)
    malformed_sig = "invalid_signature_base64"
    assert not KeyPair.verify_bytes(message, malformed_sig, keypair.get_public_key_base64())


def test_empty_message_signature():
    """Test signing and verifying empty message"""
    keypair = KeyPair()
    empty_message = b""
    
    signature = keypair.sign_bytes(empty_message)
    assert KeyPair.verify_bytes(empty_message, signature, keypair.get_public_key_base64())


def test_large_message_signature():
    """Test signing and verifying large message"""
    keypair = KeyPair()
    large_message = b"x" * 10000  # 10KB message
    
    signature = keypair.sign_bytes(large_message)
    assert KeyPair.verify_bytes(large_message, signature, keypair.get_public_key_base64())


def test_signature_with_special_characters():
    """Test signing messages with special characters"""
    keypair = KeyPair()
    special_message = b"test\x00message\nwith\tspecial\rchars"
    
    signature = keypair.sign_bytes(special_message)
    assert KeyPair.verify_bytes(special_message, signature, keypair.get_public_key_base64())
