from typing import Dict, Any, Callable, List
from acp0.core.messages import Intent, Offer, Deal, SellerInfo, Item, Price
from acp0.core.crypto import KeyPair, sign_message
from acp0.network.base import NetworkLayer

class SellerAgent:
    """卖家代理"""
    
    def __init__(self, agent_id: str, shop_name: str, 
                 inventory: Dict[str, List[Dict]], network: NetworkLayer):
        """
        Args:
            inventory: {
                "laptop": [
                    {"sku": "LTP-001", "name": "...", "price": 499900, "stock": 10, ...},
                    {"sku": "LTP-002", "name": "...", "price": 599900, "stock": 5, ...}
                ],
                "phone": [...]
            }
        """
        self.agent_id = agent_id
        self.shop_name = shop_name
        self.inventory = inventory
        self.keypair = KeyPair()
        self.network = network
        
        # 自动注册到网络
        if hasattr(network, 'register_agent'):
            network.register_agent(agent_id, "seller")
    
    def listen(self, on_deal: Callable[[Deal], None] = None):
        """
        开始监听 Intent，自动响应
        
        Args:
            on_deal: Deal 回调函数
        """
        def intent_callback(intent: Intent):
            # 验证签名和时间戳
            if not intent.verify():
                print(f"⚠️ Invalid intent: {intent.intent_id}")
                return
            
            # 检查是否有匹配的商品
            offer = self._match_intent(intent)
            if offer:
                # 签名并发送
                sign_message(offer, self.keypair)
                self.network.send_offer(offer, intent.intent_id)
                
                # 监听 Deal
                if on_deal:
                    self.network.listen_deals(offer.offer_id, on_deal)
        
        self.network.listen_intents(intent_callback)
    
    def _match_intent(self, intent: Intent) -> Offer | None:
        """匹配 Intent，从多个 SKU 中选择最优"""
        category = intent.demand.category
        
        # 1. 获取该类目下的所有商品
        products = self.inventory.get(category, [])
        if not products:
            return None
        
        # 2. 按预算筛选
        budget_min = intent.demand.budget.min
        budget_max = intent.demand.budget.max
        
        candidates = [
            p for p in products 
            if budget_min <= p['price'] <= budget_max and p['stock'] > 0
        ]
        
        if not candidates:
            return None
        
        # 3. 选择价格最低的（简单策略，可扩展）
        best_product = min(candidates, key=lambda p: p['price'])
        
        # 4. 生成 Offer
        return Offer(
            intent_id=intent.intent_id,
            seller=SellerInfo(
                agent_id=self.agent_id,
                name=self.shop_name,
                public_key=self.keypair.get_public_key_base64()
            ),
            item=Item(
                name=best_product['name'],
                sku=best_product['sku'],
                attributes=best_product.get('attributes')
            ),
            price=Price(
                amount=best_product['price'],
                currency=intent.demand.budget.currency
            ),
            stock=best_product['stock']
        )
