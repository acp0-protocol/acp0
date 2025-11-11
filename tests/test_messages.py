"""Test cases for messages module"""

import pytest
import time
from datetime import datetime
from acp0.core.messages import (
    ACPMessage, Intent, Offer, Deal, BuyerInfo, SellerInfo, 
    Demand, Budget, Item, Price, Payment, is_timestamp_valid
)
from acp0.core.crypto import KeyPair


def test_timestamp_validation():
    """Test timestamp boundary conditions"""
    now = int(time.time())
    
    # Current time should be valid
    assert is_timestamp_valid(now)
    
    # 59 seconds ago should be valid
    assert is_timestamp_valid(now - 59)
    
    # 61 seconds ago should be invalid
    assert not is_timestamp_valid(now - 61)
    
    # Future 59 seconds should be valid
    assert is_timestamp_valid(now + 59)
    
    # Future 61 seconds should be invalid
    assert not is_timestamp_valid(now + 61)
    
    # Test with custom tolerance
    assert is_timestamp_valid(now - 30, tolerance_seconds=30)
    assert not is_timestamp_valid(now - 31, tolerance_seconds=30)


def test_intent_creation_and_verification():
    """Test Intent creation and verification"""
    keypair = KeyPair()
    
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=1000, max=2000, currency="CNY")
        )
    )
    
    # Test timestamp is set
    assert intent.timestamp is not None
    assert abs(intent.timestamp - int(time.time())) <= 5
    
    # Test nonce is set and unique
    assert intent.nonce is not None
    assert len(intent.nonce) > 0
    
    # Test signature before signing
    assert intent.signature is None
    assert not intent.verify()
    
    # Test signing and verification
    intent.sign(keypair)
    assert intent.signature is not None
    assert intent.verify()
    
    # Test get_signer_public_key
    assert intent.get_signer_public_key() == keypair.get_public_key_base64()


def test_offer_creation_and_verification():
    """Test Offer creation and verification"""
    keypair = KeyPair()
    
    offer = Offer(
        intent_id="test_intent_id",
        seller=SellerInfo(
            agent_id="test_seller",
            name="Test Shop",
            public_key=keypair.get_public_key_base64()
        ),
        item=Item(
            name="Test Laptop",
            sku="TEST-001",
            attributes={"cpu": "i7", "ram": "16GB"}
        ),
        price=Price(amount=150000, currency="CNY"),
        stock=10
    )
    
    # Test timestamp and nonce
    assert offer.timestamp is not None
    assert offer.nonce is not None
    
    # Test signing and verification
    offer.sign(keypair)
    assert offer.verify()
    assert offer.get_signer_public_key() == keypair.get_public_key_base64()


def test_deal_creation_and_verification():
    """Test Deal creation and verification"""
    keypair = KeyPair()
    
    deal = Deal(
        offer_id="test_offer_id",
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        payment=Payment(
            method="mock",
            status="pending",
            token="mock_tx_001"
        )
    )
    
    # Test timestamp and nonce
    assert deal.timestamp is not None
    assert deal.nonce is not None
    
    # Test signing and verification
    deal.sign(keypair)
    assert deal.verify()
    assert deal.get_signer_public_key() == keypair.get_public_key_base64()


def test_canonical_bytes_generation():
    """Test canonical bytes generation for signing"""
    keypair = KeyPair()
    
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=1000, max=2000, currency="CNY")
        )
    )
    
    # Generate canonical bytes
    canonical_bytes = intent.to_canonical_bytes()
    
    # Should be bytes
    assert isinstance(canonical_bytes, bytes)
    
    # Should not contain signature field
    canonical_str = canonical_bytes.decode('utf-8')
    assert 'signature' not in canonical_str
    
    # Should be valid JSON
    import json
    parsed = json.loads(canonical_str)
    assert 'acp_version' in parsed
    assert 'message_type' in parsed
    assert 'buyer' in parsed


def test_nonce_uniqueness():
    """Test nonce uniqueness across multiple messages"""
    keypair = KeyPair()
    
    # Create multiple intents
    intents = []
    for i in range(10):
        intent = Intent(
            buyer=BuyerInfo(
                agent_id=f"buyer_{i}",
                public_key=keypair.get_public_key_base64()
            ),
            demand=Demand(
                category="laptop",
                budget=Budget(min=1000, max=2000, currency="CNY")
            )
        )
        intents.append(intent)
    
    # All nonces should be unique
    nonces = [intent.nonce for intent in intents]
    assert len(set(nonces)) == len(nonces)


def test_expired_timestamp_verification():
    """Test verification fails with expired timestamp"""
    keypair = KeyPair()
    
    # Create intent with expired timestamp
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=1000, max=2000, currency="CNY")
        ),
        timestamp=int(time.time()) - 120  # 2 minutes ago
    )
    
    intent.sign(keypair)
    
    # Should fail verification due to expired timestamp
    assert not intent.verify()


def test_future_timestamp_verification():
    """Test verification fails with future timestamp"""
    keypair = KeyPair()
    
    # Create intent with future timestamp
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=1000, max=2000, currency="CNY")
        ),
        timestamp=int(time.time()) + 120  # 2 minutes in future
    )
    
    intent.sign(keypair)
    
    # Should fail verification due to future timestamp
    assert not intent.verify()
