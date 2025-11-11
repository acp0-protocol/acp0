"""
In-Memory Network Layer for Demo

WARNING: NOT thread-safe!
- This implementation uses list.append() and dict access without locks
- Intended for single-threaded demonstration only
- Production use requires threading.Lock or asyncio-based implementation

For production, see: acp0/network/http.py (Phase 2)
"""

from typing import Dict, List, Callable
from acp0.network.base import NetworkLayer
from acp0.core.messages import Intent, Offer, Deal

class InMemoryNetwork(NetworkLayer):
    """内存版网络层，用于本地 Demo"""
    
    def __init__(self):
        self.intent_listeners: List[Callable] = []
        self.offer_callbacks: Dict[str, List[Callable]] = {}
        self.deal_callbacks: Dict[str, List[Callable]] = {}
        self.agents: Dict[str, str] = {}  # agent_id -> agent_type
        self.messages: Dict[str, List[Dict]] = {}  # agent_id -> list of messages
    
    def broadcast_intent(self, intent: Intent):
        """广播给所有监听者"""
        for listener in self.intent_listeners:
            listener(intent)
    
    def send_offer(self, offer: Offer, intent_id: str):
        """发送给监听该 intent_id 的回调"""
        if intent_id in self.offer_callbacks:
            for callback in self.offer_callbacks[intent_id]:
                callback(offer)
    
    def send_deal(self, deal: Deal, offer_id: str):
        """发送 Deal"""
        if offer_id in self.deal_callbacks:
            for callback in self.deal_callbacks[offer_id]:
                callback(deal)
    
    def listen_intents(self, callback: Callable[[Intent], None]):
        """注册 Intent 监听器"""
        self.intent_listeners.append(callback)
    
    def listen_offers(self, intent_id: str, callback: Callable[[Offer], None]):
        """注册 Offer 监听器"""
        if intent_id not in self.offer_callbacks:
            self.offer_callbacks[intent_id] = []
        self.offer_callbacks[intent_id].append(callback)
    
    def listen_deals(self, offer_id: str, callback: Callable[[Deal], None]):
        """注册 Deal 监听器"""
        if offer_id not in self.deal_callbacks:
            self.deal_callbacks[offer_id] = []
        self.deal_callbacks[offer_id].append(callback)
    
    def register_agent(self, agent_id: str, agent_type: str):
        """注册代理到网络"""
        self.agents[agent_id] = agent_type
        self.messages[agent_id] = []
    
    def get_messages(self, agent_id: str) -> List[Dict]:
        """获取指定代理的消息"""
        return self.messages.get(agent_id, [])
    
    def broadcast(self, message: Dict, message_type: str):
        """广播消息给所有相关代理"""
        # 记录消息到所有代理的消息历史
        for agent_id in self.agents:
            self.messages[agent_id].append({
                "type": message_type,
                "data": message,
                "timestamp": "mock_timestamp"
            })
    
    def send_message(self, target_agent_id: str, message: Dict, message_type: str):
        """发送消息给指定代理"""
        # 如果代理不存在，创建消息队列
        if target_agent_id not in self.messages:
            self.messages[target_agent_id] = []
        
        self.messages[target_agent_id].append({
            "type": message_type,
            "data": message,
            "timestamp": "mock_timestamp"
        })
    
    def clear_messages(self, agent_id: str = None):
        """清除消息历史"""
        if agent_id:
            if agent_id in self.messages:
                self.messages[agent_id] = []
        else:
            # 清除所有消息
            for agent_id in self.messages:
                self.messages[agent_id] = []
