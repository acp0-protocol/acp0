"""Test cases for agents module"""

import pytest
from acp0.agents.buyer import BuyerAgent
from acp0.agents.seller import SellerAgent
from acp0.network.memory import InMemoryNetwork
from acp0.core.messages import Intent, Demand, Budget, BuyerInfo
from acp0.core.crypto import KeyPair


def test_buyer_agent_creation():
    """Test BuyerAgent creation and basic operations"""
    network = InMemoryNetwork()
    
    buyer = BuyerAgent(
        agent_id="test_buyer",
        network=network
    )
    
    assert buyer.agent_id == "test_buyer"
    assert buyer.keypair is not None
    assert buyer.network == network


def test_seller_agent_creation():
    """Test SellerAgent creation and basic operations"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    inventory = {
        "laptop": [
            {
                "sku": "LTP-001",
                "name": "Test Laptop",
                "price": 150000,
                "stock": 5,
                "attributes": {"cpu": "i7", "ram": "16GB"}
            }
        ]
    }
    
    seller = SellerAgent(
        agent_id="test_seller",
        shop_name="Test Shop",
        inventory=inventory,
        network=network
    )
    
    assert seller.agent_id == "test_seller"
    assert seller.shop_name == "Test Shop"
    assert seller.inventory == inventory
    assert seller.network == network


def test_seller_match_intent_success():
    """Test SellerAgent matching intent successfully"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    inventory = {
        "laptop": [
            {
                "sku": "LTP-001",
                "name": "Budget Laptop",
                "price": 120000,  # Within budget
                "stock": 5,
                "attributes": {"cpu": "i5", "ram": "8GB"}
            },
            {
                "sku": "LTP-002",
                "name": "Premium Laptop",
                "price": 250000,  # Above budget
                "stock": 3,
                "attributes": {"cpu": "i9", "ram": "32GB"}
            }
        ]
    }
    
    seller = SellerAgent(
        agent_id="test_seller",
        shop_name="Test Shop",
        inventory=inventory,
        network=network
    )
    
    # Create intent within budget
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    # Should match the budget laptop
    offer = seller._match_intent(intent)
    assert offer is not None
    assert offer.item.sku == "LTP-001"
    assert offer.price.amount == 120000


def test_seller_match_intent_no_stock():
    """Test SellerAgent matching intent with no stock"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    inventory = {
        "laptop": [
            {
                "sku": "LTP-001",
                "name": "Test Laptop",
                "price": 150000,
                "stock": 0,  # No stock
                "attributes": {"cpu": "i7", "ram": "16GB"}
            }
        ]
    }
    
    seller = SellerAgent(
        agent_id="test_seller",
        shop_name="Test Shop",
        inventory=inventory,
        network=network
    )
    
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    # Should not match due to no stock
    offer = seller._match_intent(intent)
    assert offer is None


def test_seller_match_intent_out_of_budget():
    """Test SellerAgent matching intent with out-of-budget items"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    inventory = {
        "laptop": [
            {
                "sku": "LTP-001",
                "name": "Premium Laptop",
                "price": 300000,  # Above max budget
                "stock": 5,
                "attributes": {"cpu": "i9", "ram": "32GB"}
            }
        ]
    }
    
    seller = SellerAgent(
        agent_id="test_seller",
        shop_name="Test Shop",
        inventory=inventory,
        network=network
    )
    
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    # Should not match due to price being above budget
    offer = seller._match_intent(intent)
    assert offer is None


def test_seller_match_intent_category_not_found():
    """Test SellerAgent matching intent with non-existent category"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    inventory = {
        "phone": [  # Only has phones, no laptops
            {
                "sku": "PHN-001",
                "name": "Test Phone",
                "price": 50000,
                "stock": 10,
                "attributes": {"storage": "128GB"}
            }
        ]
    }
    
    seller = SellerAgent(
        agent_id="test_seller",
        shop_name="Test Shop",
        inventory=inventory,
        network=network
    )
    
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",  # Category not in inventory
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    # Should not match due to category not found
    offer = seller._match_intent(intent)
    assert offer is None


def test_seller_multiple_sku_selection():
    """Test SellerAgent selecting best SKU from multiple options"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    inventory = {
        "laptop": [
            {
                "sku": "LTP-001",
                "name": "Budget Laptop",
                "price": 120000,  # Cheapest
                "stock": 5,
                "attributes": {"cpu": "i5", "ram": "8GB"}
            },
            {
                "sku": "LTP-002",
                "name": "Mid-range Laptop",
                "price": 180000,
                "stock": 3,
                "attributes": {"cpu": "i7", "ram": "16GB"}
            },
            {
                "sku": "LTP-003",
                "name": "Premium Laptop",
                "price": 250000,  # Too expensive
                "stock": 2,
                "attributes": {"cpu": "i9", "ram": "32GB"}
            }
        ]
    }
    
    seller = SellerAgent(
        agent_id="test_seller",
        shop_name="Test Shop",
        inventory=inventory,
        network=network
    )
    
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="test_buyer",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    # Should select the cheapest available option (LTP-001)
    offer = seller._match_intent(intent)
    assert offer is not None
    assert offer.item.sku == "LTP-001"
    assert offer.price.amount == 120000


def test_buyer_broadcast_intent():
    """Test BuyerAgent broadcasting intent"""
    network = InMemoryNetwork()
    
    buyer = BuyerAgent(
        agent_id="test_buyer",
        network=network
    )
    
    # Test broadcasting intent
    offers = buyer.broadcast(
        category="laptop",
        budget_range=(100000, 200000),
        location="shanghai"
    )
    
    # Should return empty list if no sellers respond
    assert isinstance(offers, list)
    assert len(offers) == 0


def test_agent_network_registration():
    """Test agents registering with network"""
    network = InMemoryNetwork()
    
    # Create buyer and seller
    buyer = BuyerAgent(
        agent_id="test_buyer",
        network=network
    )
    
    seller = SellerAgent(
        agent_id="test_seller",
        shop_name="Test Shop",
        inventory={"laptop": []},
        network=network
    )
    
    # Both should be registered with network
    assert "test_buyer" in network.agents
    assert "test_seller" in network.agents
