from typing import List
from acp0.core.messages import Intent, Offer, Deal, BuyerInfo, Demand, Budget, Payment
from acp0.core.crypto import KeyPair, sign_message
from acp0.network.base import NetworkLayer

class BuyerAgent:
    """买家代理"""
    
    def __init__(self, agent_id: str, network: NetworkLayer):
        self.agent_id = agent_id
        self.keypair = KeyPair()  # 自动生成密钥对
        self.network = network
        self.received_offers: List[Offer] = []
        
        # 自动注册到网络
        if hasattr(network, 'register_agent'):
            network.register_agent(agent_id, "buyer")
    
    def broadcast(self, category: str, budget_range: tuple, 
                  currency: str = "CNY", **kwargs) -> List[Offer]:
        """
        广播购物需求，返回收到的 Offers
        
        NOTE: This is a SYNCHRONOUS implementation for demo simplicity.
        - Uses time.sleep(1) to wait for offers
        - Production should use async/await or callbacks
        
        TODO v1.0: Refactor to:
            async def broadcast(...) -> AsyncIterator[Offer]
        
        Args:
            category: 商品类别
            budget_range: (min, max) 元组
            currency: 货币代码
            **kwargs: 其他可选参数（location, delivery_days, attributes）
        """
        # 1. 构建 Intent
        intent = Intent(
            buyer=BuyerInfo(
                agent_id=self.agent_id,
                public_key=self.keypair.get_public_key_base64()
            ),
            demand=Demand(
                category=category,
                budget=Budget(min=budget_range[0], max=budget_range[1], currency=currency),
                **kwargs
            )
        )
        
        # 2. 签名
        sign_message(intent, self.keypair)
        
        # 3. 清空之前的 Offers
        self.received_offers = []
        
        # 4. 注册 Offer 监听器
        def offer_callback(offer: Offer):
            # 验证 Offer 签名和时间戳
            if offer.verify():
                self.received_offers.append(offer)
            else:
                print(f"⚠️ Invalid offer: {offer.offer_id}")
        
        self.network.listen_offers(intent.intent_id, offer_callback)
        
        # 5. 广播 Intent
        self.network.broadcast_intent(intent)
        
        # 6. 等待 Offers（实际应该异步，这里简化）
        import time
        time.sleep(1)  # FIXME: Replace with proper async in v1.0
        
        return self.received_offers
    
    def select_best(self, offers: List[Offer]) -> Offer:
        """选择最优 Offer（简单逻辑：价格最低）"""
        if not offers:
            raise ValueError("No offers to select from")
        
        return min(offers, key=lambda o: o.price.amount)
    
    def purchase(self, offer: Offer, payment_method: str = "mock") -> Deal:
        """确认购买"""
        deal = Deal(
            offer_id=offer.offer_id,
            buyer=BuyerInfo(
                agent_id=self.agent_id,
                public_key=self.keypair.get_public_key_base64()
            ),
            payment=Payment(
                method=payment_method,
                status="authorized",
                token="mock-token-xxx"
            )
        )
        
        # 签名
        sign_message(deal, self.keypair)
        
        # 发送
        self.network.send_deal(deal, offer.offer_id)
        
        return deal
