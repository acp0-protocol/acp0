from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import uuid4
from datetime import datetime
from abc import abstractmethod
import json
import time

def is_timestamp_valid(timestamp: int, tolerance_seconds: int = 60) -> bool:
    """
    校验时间戳是否在合理范围内
    Args:
        timestamp: 消息的 Unix 时间戳
        tolerance_seconds: 容忍偏差（默认 60 秒）
    """
    now = int(time.time())
    return abs(now - timestamp) <= tolerance_seconds


class ACPMessage(BaseModel):
    """所有 ACP 消息的基类"""
    
    acp_version: str = "0.9"
    message_type: str
    anchor_mode: str = "none"  # "none" | "hash" | "full"
    signature: Optional[str] = None
    nonce: str = Field(default_factory=lambda: str(uuid4()))  # 防重放
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    
    def to_canonical_bytes(self) -> bytes:
        """
        生成用于签名的规范化字节流
        CRITICAL: 必须排除 signature 字段，且 key 排序
        """
        data = self.model_dump(
            exclude={'signature'}, 
            exclude_none=True
        )
        canonical_json = json.dumps(
            data, 
            sort_keys=True, 
            separators=(',', ':')
        )
        return canonical_json.encode('utf-8')
    
    def sign(self, keypair):
        """给消息签名"""
        from .crypto import sign_message
        sign_message(self, keypair)
    
    @abstractmethod
    def get_signer_public_key(self) -> str:
        """
        返回签名者的公钥
        子类必须实现（Intent/Deal 返回 buyer.public_key，Offer 返回 seller.public_key）
        """
        pass
    
    def verify(self) -> bool:
        """验证消息签名 + 时间戳"""
        # 1. 时间戳校验
        if not is_timestamp_valid(self.timestamp, tolerance_seconds=60):
            return False
        
        # 2. 签名校验
        if not self.signature:
            return False
        
        from .crypto import KeyPair
        return KeyPair.verify_bytes(
            self.to_canonical_bytes(),
            self.signature,
            self.get_signer_public_key()
        )


class BuyerInfo(BaseModel):
    agent_id: str
    public_key: str  # base64 encoded

class Budget(BaseModel):
    min: int
    max: int
    currency: str

class Demand(BaseModel):
    category: str
    budget: Budget
    attributes: Optional[list[str]] = None
    location: Optional[str] = None
    delivery_days: Optional[int] = None

class Intent(ACPMessage):
    message_type: str = "intent"
    intent_id: str = Field(default_factory=lambda: str(uuid4()))
    buyer: BuyerInfo
    demand: Demand
    expires_at: Optional[int] = None
    
    def get_signer_public_key(self) -> str:
        return self.buyer.public_key

class SellerInfo(BaseModel):
    agent_id: str
    name: str
    public_key: str

class Item(BaseModel):
    name: str
    sku: str
    images: Optional[list[str]] = None
    attributes: Optional[Dict[str, Any]] = None

class Price(BaseModel):
    amount: int  # cents
    currency: str

class Offer(ACPMessage):
    message_type: str = "offer"
    offer_id: str = Field(default_factory=lambda: str(uuid4()))
    intent_id: str
    seller: SellerInfo
    item: Item
    price: Price
    stock: int
    expires_at: Optional[int] = None
    
    def get_signer_public_key(self) -> str:
        return self.seller.public_key

class Payment(BaseModel):
    method: str
    status: str
    token: Optional[str] = None

class Deal(ACPMessage):
    message_type: str = "deal"
    deal_id: str = Field(default_factory=lambda: str(uuid4()))
    offer_id: str
    buyer: BuyerInfo
    payment: Payment
    
    def get_signer_public_key(self) -> str:
        return self.buyer.public_key
