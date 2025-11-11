"""Test cases for network module"""

import pytest
from acp0.network.memory import InMemoryNetwork
from acp0.core.messages import Intent, Offer, Deal, BuyerInfo, SellerInfo, Demand, Budget, Item, Price, Payment
from acp0.core.crypto import KeyPair


def test_network_creation():
    """Test InMemoryNetwork creation"""
    network = InMemoryNetwork()
    
    assert network.agents == {}
    assert network.messages == {}


def test_register_agent():
    """Test registering agents with network"""
    network = InMemoryNetwork()
    
    # Register buyer
    network.register_agent("buyer_001", "buyer")
    assert "buyer_001" in network.agents
    assert network.agents["buyer_001"] == "buyer"
    
    # Register seller
    network.register_agent("seller_001", "seller")
    assert "seller_001" in network.agents
    assert network.agents["seller_001"] == "seller"


def test_broadcast_message():
    """Test broadcasting messages to all agents"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    # Register multiple agents
    network.register_agent("buyer_001", "buyer")
    network.register_agent("seller_001", "seller")
    network.register_agent("seller_002", "seller")
    
    # Create a test message
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="buyer_001",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    # Broadcast message
    network.broadcast(intent, "intent")
    
    # Should be recorded in messages
    assert len(network.messages) == 3  # 3 agents registered
    for agent_id in ["buyer_001", "seller_001", "seller_002"]:
        messages = network.get_messages(agent_id)
        assert len(messages) == 1
        assert messages[0]["type"] == "intent"
        assert messages[0]["data"] == intent


def test_send_message_to_specific_agent():
    """Test sending message to specific agent"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    # Register agents
    network.register_agent("buyer_001", "buyer")
    network.register_agent("seller_001", "seller")
    
    # Create a test message
    offer = Offer(
        intent_id="test_intent",
        seller=SellerInfo(
            agent_id="seller_001",
            name="Test Shop",
            public_key=keypair.get_public_key_base64()
        ),
        item=Item(
            name="Test Laptop",
            sku="TEST-001",
            attributes={"cpu": "i7"}
        ),
        price=Price(amount=150000, currency="CNY"),
        stock=5
    )
    
    # Send message to specific agent
    network.send_message("buyer_001", offer, "offer")
    
    # Should be recorded in messages
    messages = network.get_messages("buyer_001")
    assert len(messages) == 1
    assert messages[0]["type"] == "offer"
    assert messages[0]["data"] == offer


def test_get_messages_for_agent():
    """Test retrieving messages for specific agent"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    # Register agents
    network.register_agent("buyer_001", "buyer")
    network.register_agent("seller_001", "seller")
    
    # Create and send multiple messages
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="buyer_001",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    offer = Offer(
        intent_id=intent.intent_id,
        seller=SellerInfo(
            agent_id="seller_001",
            name="Test Shop",
            public_key=keypair.get_public_key_base64()
        ),
        item=Item(
            name="Test Laptop",
            sku="TEST-001",
            attributes={"cpu": "i7"}
        ),
        price=Price(amount=150000, currency="CNY"),
        stock=5
    )
    
    deal = Deal(
        offer_id=offer.offer_id,
        buyer=BuyerInfo(
            agent_id="buyer_001",
            public_key=keypair.get_public_key_base64()
        ),
        payment=Payment(
            method="mock",
            status="pending"
        )
    )
    
    # Send messages
    network.broadcast(intent, "intent")  # To all agents
    network.send_message("buyer_001", offer, "offer")  # To buyer only
    network.send_message("seller_001", deal, "deal")  # To seller only
    
    # Test message retrieval
    buyer_messages = network.get_messages("buyer_001")
    seller_messages = network.get_messages("seller_001")
    
    # Buyer should receive broadcast intent and direct offer
    assert len(buyer_messages) == 2
    assert any(msg["data"] == intent for msg in buyer_messages)
    assert any(msg["data"] == offer for msg in buyer_messages)
    
    # Seller should receive broadcast intent and direct deal
    assert len(seller_messages) == 2
    assert any(msg["data"] == intent for msg in seller_messages)
    assert any(msg["data"] == deal for msg in seller_messages)


def test_clear_messages():
    """Test clearing messages for specific agent"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    # Register agent and send messages
    network.register_agent("buyer_001", "buyer")
    
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="buyer_001",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    network.broadcast(intent, "intent")
    
    # Should have messages initially
    assert len(network.get_messages("buyer_001")) == 1
    
    # Clear messages
    network.clear_messages("buyer_001")
    
    # Should have no messages after clearing
    assert len(network.get_messages("buyer_001")) == 0
    
    # Global messages dict should still contain the agent entry
    assert "buyer_001" in network.messages


def test_agent_not_found():
    """Test behavior when agent is not registered"""
    network = InMemoryNetwork()
    
    # Getting messages for non-existent agent should return empty list
    messages = network.get_messages("non_existent_agent")
    assert messages == []
    
    # Clearing messages for non-existent agent should not raise error
    network.clear_messages("non_existent_agent")
    
    # Sending message to non-existent agent should still record the message
    keypair = KeyPair()
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="buyer_001",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    network.send_message("non_existent_agent", intent, "intent")
    assert len(network.messages) == 1


def test_message_ordering():
    """Test that messages are maintained in order"""
    network = InMemoryNetwork()
    keypair = KeyPair()
    
    network.register_agent("test_agent", "test")
    
    # Create multiple messages
    messages = []
    for i in range(5):
        intent = Intent(
            buyer=BuyerInfo(
                agent_id=f"buyer_{i}",
                public_key=keypair.get_public_key_base64()
            ),
            demand=Demand(
                category="laptop",
                budget=Budget(min=100000, max=200000, currency="CNY")
            )
        )
        messages.append(intent)
        network.send_message("test_agent", intent, "intent")
    
    # Retrieve messages and check order
    retrieved_messages = network.get_messages("test_agent")
    assert len(retrieved_messages) == 5
    
    # Check that messages are in order and contain the expected data
    for i, retrieved_msg in enumerate(retrieved_messages):
        assert retrieved_msg["data"] == messages[i]
        assert retrieved_msg["type"] == "intent"


def test_broadcast_to_multiple_agent_types():
    """Test broadcasting to agents of different types"""
    network = InMemoryNetwork()
    
    # Register agents of different types
    network.register_agent("buyer_001", "buyer")
    network.register_agent("seller_001", "seller")
    network.register_agent("logistics_001", "logistics")
    
    keypair = KeyPair()
    intent = Intent(
        buyer=BuyerInfo(
            agent_id="buyer_001",
            public_key=keypair.get_public_key_base64()
        ),
        demand=Demand(
            category="laptop",
            budget=Budget(min=100000, max=200000, currency="CNY")
        )
    )
    
    # Broadcast should reach all agents
    network.broadcast(intent, "intent")
    
    # All agents should receive the broadcast message
    for agent_id in ["buyer_001", "seller_001", "logistics_001"]:
        messages = network.get_messages(agent_id)
        assert len(messages) == 1
        assert messages[0]["data"] == intent
        assert messages[0]["type"] == "intent"
