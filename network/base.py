from abc import ABC, abstractmethod
from typing import Callable
from acp0.core.messages import Intent, Offer, Deal

class NetworkLayer(ABC):
    """网络层抽象基类"""
    
    @abstractmethod
    def broadcast_intent(self, intent: Intent):
        """广播 Intent"""
        pass
    
    @abstractmethod
    def send_offer(self, offer: Offer, intent_id: str):
        """发送 Offer 给特定买家"""
        pass
    
    @abstractmethod
    def send_deal(self, deal: Deal, offer_id: str):
        """发送 Deal 给特定卖家"""
        pass
    
    @abstractmethod
    def listen_intents(self, callback: Callable[[Intent], None]):
        """监听 Intent 消息"""
        pass
    
    @abstractmethod
    def listen_offers(self, intent_id: str, callback: Callable[[Offer], None]):
        """监听特定 Intent 的 Offer"""
        pass
