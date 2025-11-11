class ACP0Error(Exception):
    """ACP0 基础异常"""
    pass

class SignatureError(ACP0Error):
    """签名验证失败"""
    pass

class NetworkError(ACP0Error):
    """网络通信错误"""
    pass

class MessageValidationError(ACP0Error):
    """消息验证失败"""
    pass
