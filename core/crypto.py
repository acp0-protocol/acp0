import hashlib
import base64
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import sigencode_der, sigdecode_der

class KeyPair:
    """
    ECC Key Pair for signing and verification
    
    SECURITY WARNING:
    - This demo generates a NEW keypair on every run
    - Production MUST load from encrypted PEM file with 600 permission
    - Example:
        keypair = KeyPair.from_pem_file('~/.acp0/private.pem')
    
    TODO v1.0: Implement persistent key management
    """
    
    def __init__(self, private_key: SigningKey = None):
        if private_key is None:
            # 生成新密钥对
            self.private_key = SigningKey.generate(curve=SECP256k1)
        else:
            self.private_key = private_key
        
        self.public_key = self.private_key.get_verifying_key()
    
    def get_public_key_base64(self) -> str:
        """返回 base64 编码的公钥"""
        return base64.b64encode(
            self.public_key.to_string()
        ).decode('utf-8')
    
    def get_private_key_base64(self) -> str:
        """返回 base64 编码的私钥"""
        return base64.b64encode(
            self.private_key.to_string()
        ).decode('utf-8')
    
    def sign(self, message: str) -> str:
        """对消息签名，返回 base64 编码的签名"""
        # 1. 计算 SHA256 哈希
        message_hash = hashlib.sha256(message.encode('utf-8')).digest()
        
        # 2. 用私钥签名
        signature = self.private_key.sign_digest(
            message_hash,
            sigencode=sigencode_der
        )
        
        # 3. Base64 编码
        return base64.b64encode(signature).decode('utf-8')
    
    def sign_bytes(self, data: bytes) -> str:
        """对字节流签名（改名，更明确）"""
        message_hash = hashlib.sha256(data).digest()
        signature = self.private_key.sign_digest(
            message_hash,
            sigencode=sigencode_der
        )
        return base64.b64encode(signature).decode('utf-8')
    
    @staticmethod
    def verify(message: str, signature_b64: str, public_key_b64: str) -> bool:
        """验证签名"""
        try:
            # 1. 解码公钥和签名
            public_key_bytes = base64.b64decode(public_key_b64)
            signature_bytes = base64.b64decode(signature_b64)
            
            # 2. 重建公钥对象
            verifying_key = VerifyingKey.from_string(
                public_key_bytes,
                curve=SECP256k1
            )
            
            # 3. 计算消息哈希
            message_hash = hashlib.sha256(message.encode('utf-8')).digest()
            
            # 4. 验证签名
            verifying_key.verify_digest(
                signature_bytes,
                message_hash,
                sigdecode=sigdecode_der
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    def verify_bytes(data: bytes, signature_b64: str, public_key_b64: str) -> bool:
        """验证字节流签名"""
        try:
            public_key_bytes = base64.b64decode(public_key_b64)
            signature_bytes = base64.b64decode(signature_b64)
            
            verifying_key = VerifyingKey.from_string(
                public_key_bytes,
                curve=SECP256k1
            )
            
            message_hash = hashlib.sha256(data).digest()
            verifying_key.verify_digest(
                signature_bytes,
                message_hash,
                sigdecode=sigdecode_der
            )
            return True
        except Exception:
            return False

def sign_message(message_obj, keypair: KeyPair):
    """给消息对象签名（Intent/Offer/Deal）"""
    canonical_bytes = message_obj.to_canonical_bytes()
    signature = keypair.sign_bytes(canonical_bytes)
    message_obj.signature = signature
    return message_obj

# 删除原来的 verify_message()，改用消息自带的 msg.verify()
