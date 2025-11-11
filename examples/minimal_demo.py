"""
ACP0 Minimal Demo - 最简单的双 Agent 交易示例

预期输出:
---------
>>> ACP0 Minimal Demo Starting...

[SETUP] Setting up Seller Agent...
[OK] Seller is listening for Intents...

[SETUP] Setting up Buyer Agent...
[OK] Buyer is ready

[BROADCAST] Buyer broadcasting Intent...
   Category: laptop
   Budget: 4000-6000 CNY
   Location: shanghai

[RESULT] Received 2 offer(s)

[SELECT] Best Offer Selected:
   Seller: Tech Paradise
   Product: Laptop Pro 14 2025 (16G)
   Price: CNY 4999.00
   Stock: 10

[PAYMENT] Buyer confirming purchase...
[OK] Deal confirmed: 9d4e5f6g-...
[OK] Seller received Deal: 9d4e5f6g-...
   Payment: mock-payment

[SUCCESS] Transaction Complete!
   Intent → Offer → Deal flow successful

运行时间: ~1-2 秒
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from acp0.agents.buyer import BuyerAgent
from acp0.agents.seller import SellerAgent
from acp0.network.memory import InMemoryNetwork

def main():
    print(">>> ACP0 Minimal Demo Starting...")
    print()
    
    # 1. 创建网络层
    network = InMemoryNetwork()
    
    # 2. 设置卖家代理（改进的库存格式）
    seller_inventory = {
        "laptop": [
            {
                "sku": "LTP-2025-16G-512G",
                "name": "Laptop Pro 14 2025 (16G)",
                "price": 499900,  # CNY 4999.00
                "stock": 10,
                "attributes": {
                    "cpu": "R7-8840U",
                    "ram": "16GB",
                    "ssd": "512GB"
                }
            },
            {
                "sku": "LTP-2025-32G-1T",
                "name": "Laptop Pro 14 2025 (32G)",
                "price": 599900,  # CNY 5999.00
                "stock": 5,
                "attributes": {
                    "cpu": "R7-8840U",
                    "ram": "32GB",
                    "ssd": "1TB"
                }
            }
        ]
    }
    
    print("[SETUP] Setting up Seller Agent...")
    seller = SellerAgent(
        agent_id="seller-001",
        shop_name="Tech Paradise",
        inventory=seller_inventory,
        network=network
    )
    
    # 卖家开始监听
    def on_deal_received(deal):
        print(f"[OK] Seller received Deal: {deal.deal_id[:12]}...")
        print(f"   Payment: {deal.payment.method}")
    
    seller.listen(on_deal=on_deal_received)
    print("[OK] Seller is listening for Intents...")
    print()
    
    # 3. 设置买家代理
    print("[SETUP] Setting up Buyer Agent...")
    buyer = BuyerAgent(agent_id="buyer-001", network=network)
    print("[OK] Buyer is ready")
    print()
    
    # 4. 买家广播需求
    print("[BROADCAST] Buyer broadcasting Intent...")
    print("   Category: laptop")
    print("   Budget: 4000-6000 CNY")
    print("   Location: shanghai")
    print()
    
    offers = buyer.broadcast(
        category="laptop",
        budget_range=(400000, 600000),  # 4000-6000 元（以分为单位）
        currency="CNY",
        location="shanghai"
    )
    
    print(f"[RESULT] Received {len(offers)} offer(s)")
    print()
    
    if not offers:
        print("❌ No offers received")
        return
    
    # 5. 选择最优报价
    best_offer = buyer.select_best(offers)
    print("[SELECT] Best Offer Selected:")
    print(f"   Seller: {best_offer.seller.name}")
    print(f"   Product: {best_offer.item.name}")
    print(f"   Price: CNY {best_offer.price.amount / 100:.2f}")
    print(f"   Stock: {best_offer.stock}")
    print()
    
    # 6. 确认购买
    print("[PAYMENT] Buyer confirming purchase...")
    deal = buyer.purchase(best_offer, payment_method="mock-payment")
    print(f"[OK] Deal confirmed: {deal.deal_id[:12]}...")
    print()
    
    print("[SUCCESS] Transaction Complete!")
    print("   Intent → Offer → Deal flow successful")
    print()
    print("运行时间: ~1-2 秒")

if __name__ == "__main__":
    main()
