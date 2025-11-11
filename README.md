# ACP0 - Agent Commerce Protocol

一个基于智能体的商业协议实现，支持意图、报价和交易的消息传递。

## 项目概述

ACP0 (Agent Commerce Protocol) 是一个轻量级的商业协议框架，允许智能体之间进行安全的商业交互。该项目实现了：

- **消息协议**：Intent（意图）、Offer（报价）、Deal（交易）消息类型
- **加密签名**：基于ECDSA的数字签名和验证
- **时间戳验证**：防重放攻击的时间戳机制
- **网络抽象**：支持内存网络和可扩展的网络实现

## 功能特性

- 🔐 **安全通信**：所有消息都经过数字签名和时间戳验证
- 🏗️ **模块化设计**：核心协议与网络实现分离
- 🧪 **完整测试**：包含单元测试和集成测试
- 📦 **易于使用**：清晰的API和示例代码

## 项目结构

```
acp0/
├── core/                 # 核心协议实现
│   ├── messages.py      # 消息定义和验证
│   ├── crypto.py        # 加密和签名功能
│   └── exceptions.py    # 异常定义
├── agents/              # 智能体实现
│   ├── buyer.py         # 买家智能体
│   └── seller.py        # 卖家智能体
├── network/             # 网络层抽象
│   ├── base.py          # 网络基类
│   └── memory.py        # 内存网络实现
├── tests/               # 测试套件
├── examples/            # 使用示例
└── scripts/             # 运行脚本
```

## 快速开始

### 安装依赖

```bash
pip install pydantic ecdsa
```

### 运行示例

```bash
# 运行最小演示
python scripts/run_demo.py

# 或者使用shell脚本
./scripts/run_demo.sh
```

### 基本用法

```python
from core.messages import Intent, Offer, Deal
from core.crypto import KeyPair
from agents.buyer import BuyerAgent
from agents.seller import SellerAgent

# 创建智能体
buyer = BuyerAgent()
seller = SellerAgent()

# 创建意图
intent = buyer.create_intent(
    category="electronics",
    min_budget=10000,
    max_budget=50000,
    currency="CNY"
)

# 创建报价
offer = seller.create_offer(intent)

# 创建交易
deal = buyer.create_deal(offer)
```

## 消息类型

### Intent（意图）
- 买家表达购买意愿
- 包含预算、品类、交付要求等信息

### Offer（报价）
- 卖家响应意图的报价
- 包含商品信息、价格、库存等

### Deal（交易）
- 买家接受报价的交易确认
- 包含支付信息等

## 安全特性

- **数字签名**：所有消息都使用ECDSA进行签名
- **时间戳验证**：防止重放攻击
- **Nonce机制**：确保消息唯一性
- **规范化序列化**：签名前对消息进行规范化处理

## 开发

### 运行测试

```bash
python -m pytest tests/ -v
```

### 代码规范

项目使用pytest进行测试，遵循Python PEP 8编码规范。

## 许可证

[在此添加许可证信息]

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。
