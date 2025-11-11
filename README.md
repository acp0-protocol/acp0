# ACP0: Agent-Commerce Protocol

**The HTTP of AI Shopping / AI 购物的 HTTP 协议**

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.9.0%20MVP-orange.svg)](https://github.com/acp0/acp0/releases)
[![Tests](https://img.shields.io/badge/tests-32%20passed-brightgreen.svg)](tests/)

> Open standard for AI-to-AI commerce. Let buyer agents and seller agents negotiate directly, no platform needed.
> 
> AI 对 AI 购物的开放标准协议。让买家代理与卖家代理直接协商，无需平台中介。

---

## ⚡ Why ACP0 is Fast (Not Another Slow Blockchain App)

**ACP0 is NOT a blockchain e-commerce platform.**

It's a **high-speed off-chain protocol** with optional on-chain anchoring:

- 💨 **99% traffic**: MQTT/HTTP messaging (< 50ms latency)
- ⛓️ **1% traffic**: Blockchain hashes for dispute resolution  
- 🚫 **0% dependency**: Works without any blockchain at all

**Think of it as:**
- 📡 **Broadcast**: MQTT (like WhatsApp for agents)
- 🏛️ **Trust**: Blockchain (like notary, only used when disputes happen)

**Example - Buying a $500 laptop:**

```
1. Your agent broadcasts intent via MQTT     →  0ms,  $0
2. 10 sellers respond in 50ms                →  Off-chain
3. You buy with Stripe                       →  Off-chain
4. Optional: Store deal hash on Arbitrum     →  $0.0002
```

**Blockchain is the "stone tablet on the roadside", not the highway.**

---

## 🚀 Current Status: v0.9.0 (MVP)

**What's Ready:**
- ✅ Complete protocol specification (Intent/Offer/Deal)
- ✅ ECC signature and verification
- ✅ Reference implementation with 32 passing tests
- ✅ Working demo (1-2s transaction time)

**What's Coming in v1.0 (Q1 2025):**
- 🚧 MQTT network layer (real-time broadcast)
- 🚧 HTTP Indexer (distributed discovery)
- 🚧 Blockchain anchoring (optional trust layer)
- 🚧 Async/await refactoring

**What This Means:**
v0.9.0 proves the protocol works. It's ready for:
- ✅ Protocol discussion and feedback
- ✅ Academic research
- ✅ Building proof-of-concepts
- ❌ Not yet for production e-commerce (wait for v1.0)

See [ROADMAP.md](ROADMAP.md) for the full plan.

---

## 🎯 What is ACP0?

### The Story Behind It

In November 2024, **Amazon sued Perplexity** for building "Comet" - an AI agent that logs into Amazon, compares products, and buys based on *real user needs* instead of *paid ads*.

Amazon's lawsuit revealed a fundamental conflict:
- **Platforms want control**: They make money from ads and recommendations
- **Users want agents**: AI that works for them, not for advertisers

**ACP0 is the answer**: What if agents don't need platforms at all?

### How It Works

```
┌─────────────┐                                    ┌─────────────┐
│ Buyer Agent │─────── 1. Broadcast Intent ───────▶│  MQTT/HTTP  │
│  (User AI)  │                                    │   Network   │
└─────────────┘                                    └─────────────┘
       ▲                                                  │
       │                                                  │ 2. Forward
       │                                                  ▼
       │                                           ┌─────────────┐
       │                                           │Seller Agent │
       │                                           │Seller Agent │
       │                                           │Seller Agent │
       │                                           └─────────────┘
       │                                                  │
       │                                                  │ 3. Send Offers
       │                                                  ▼
       └───────────── 4. Compare & Select ───────────────┘
                            │
                            │ 5. Payment & Delivery
                            ▼
                      [Transaction Complete]
```

**Core Components:**
- **Intent**: Structured shopping request (JSON)
- **Offer**: Merchant's response with price, stock, delivery
- **Deal**: Payment and fulfillment confirmation
- **Signature**: ECC-based verification (no middleman needed)

---

## ⚡ Quick Start

### Installation

```bash
pip install acp0
```

### Buyer Agent (3 lines)

```python
from acp0 import BuyerAgent

agent = BuyerAgent()
offers = agent.broadcast(
    category="laptop",
    budget_range=(4000, 6000),
    currency="CNY",
    location="shanghai"
)

best = agent.select_best(offers)
agent.purchase(best)
```

### Seller Agent (3 lines)

```python
from acp0 import SellerAgent

agent = SellerAgent(
    name="MyShop",
    inventory="./products.json",
    location="shanghai"
)

agent.listen()  # Start receiving intents and auto-respond
```

**That's it!** Two agents just completed a transaction without any platform.

### Run the Demo

```bash
# Clone the repository
git clone https://github.com/acp0/acp0.git
cd acp0

# Install dependencies
pip install -e .

# Run minimal demo
python examples/minimal_demo.py
```

**Expected output:**
```
🚀 ACP0 Minimal Demo Starting...
📦 Setting up Seller Agent...
✓ Seller is listening for Intents...
🛍️ Setting up Buyer Agent...
✓ Buyer is ready
📢 Buyer broadcasting Intent...
📬 Received 1 offer(s)
🏆 Best Offer Selected
💳 Buyer confirming purchase...
✅ Deal confirmed
🎉 Transaction Complete!
```

---

## 🌟 Key Features

### ✅ Platform-Free
- Works with WeChat shops, Shopify stores, 1688 suppliers, or any merchant
- No listing fees, no commission cuts

### ✅ Agent-First Design
- Structured JSON for AI agents (not keyword search for humans)
- Real-time negotiation between buyer AI and seller AI

### ✅ Trust Without Middlemen
- Cryptographic signatures verify every message
- Optional blockchain anchoring for disputes
- Decentralized reputation (coming in v1.0)

### ✅ Lightweight & Extensible
- Core spec: 3 message types, <500 lines of code
- Plug in any payment method (Stripe, Alipay, crypto)
- Add custom fields without breaking compatibility

---

## 📖 Documentation

**Core Documents:**
- [Protocol Specification](spec/ACP0-Core.md) - Message formats and security
- [Design Philosophy](docs/ARCHITECTURE.md) - Why 99% off-chain + 1% on-chain
- [Implementation Guide](docs/IMPLEMENTATION.md) - How to build it
- [FAQ](docs/FAQ.md) - Common questions
- [ROADMAP](ROADMAP.md) - What's next

**For Developers:**
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [API Documentation](docs/API.md) - Python SDK reference
- [Examples](examples/) - Code samples

---

## 🚀 Use Cases

### 1️⃣ WeChat Shop Discovery
**Problem:** 1M+ WeChat shops have great products but no way to be discovered by AI agents  
**Solution:** Shops implement ACP0, agents can find them via intent broadcast

### 2️⃣ Cross-Border B2B
**Problem:** Alibaba/1688 suppliers pay high platform fees  
**Solution:** Direct agent-to-agent negotiation, no middleman

### 3️⃣ Private Domain Commerce
**Problem:** Influencers sell via manual messages (inefficient)  
**Solution:** Deploy a seller agent, handle inquiries 24/7

### 4️⃣ AI Shopping Assistants
**Problem:** Today's AI can only search Amazon/Taobao (controlled by ads)  
**Solution:** Access decentralized merchant network with better prices

---

## 🛠️ Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| **Core Protocol** | ✅ Complete | Intent/Offer/Deal messages |
| **Signatures** | ✅ Complete | ECC-based verification |
| **Agents** | ✅ Complete | Buyer and Seller logic |
| **In-Memory Network** | ✅ Complete | Demo/testing only |
| **MQTT Network** | 🚧 Planned v1.0 | Real-time broadcast |
| **HTTP Indexer** | 🚧 Planned v1.0 | Distributed discovery |
| **Blockchain** | 🚧 Planned v1.0 | Optional anchoring |
| **Smart Contracts** | 📋 Planned v2.0 | Dispute resolution |

See [ROADMAP.md](ROADMAP.md) for detailed plans.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=acp0 --cov-report=term-missing

# Run specific test
pytest tests/test_messages.py -v
```

**Current Test Status:**
- ✅ 32 tests passing
- ✅ 100% pass rate
- ✅ Core protocol fully tested

---

## 🤝 Contributing

We welcome contributions from everyone! Here's how to get started:

1. **Read [CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines and workflow
2. **Check [Good First Issues](https://github.com/acp0/acp0/labels/good%20first%20issue)** - Easy tasks for newcomers
3. **Join the discussion** - GitHub Issues or Discussions
4. **Submit a PR** - We review within 48 hours

**Priority Areas for v1.0:**
- 🔴 MQTT network layer implementation
- 🔴 HTTP Indexer service
- 🔴 Async/await refactoring
- 🟡 Additional language SDKs (Node.js, Rust, Go)
- 🟡 Documentation improvements

---

## 🌐 Community

### Communication Channels

- **GitHub Issues** - Bug reports, feature requests, RFCs
- **GitHub Discussions** - General questions and ideas
- **Discord** - Real-time chat (coming soon)
- **Twitter** - [@acp0protocol](https://twitter.com/acp0protocol)
- **中文社区** - [即刻](https://okjk.co/acp0) | [知乎](https://zhuanlan.zhihu.com/acp0)

### Monthly RFC Meetings

**When:** First Saturday of each month, 10:00 AM UTC  
**Where:** Zoom (public, link in Discussions)  
**What:** Protocol discussions and RFC voting

---

## 🏆 Hall of Fame

🥇 **First Production Deployment:** *[Waiting for you]*  
🥈 **First Cross-Border Transaction:** *[Waiting for you]*  
🥉 **First 1M GMV Milestone:** *[Waiting for you]*  

Want your name here? Ship something awesome with ACP0!

---

## 📜 About This Project

### Created by Human + AI Collaboration

ACP0 was designed by [@deloog](https://github.com/deloog), a non-technical founder, working with Claude (Anthropic), DeepSeek, and KIMI. This project itself is a proof that:

> **If humans and AI can design protocols together, imagine what agents can achieve in commerce.**
> 
> **如果人类和 AI 能一起设计协议，想象代理在商业中能成就什么。**

### Inspiration

This project was inspired by the **Perplexity vs Amazon** case, which showed that:
- AI agents can challenge traditional platforms
- Users want agents that work for them, not for advertisers
- The future needs open protocols, not closed platforms

---

## 📄 License

- **Protocol Specification:** CC0-1.0 (Public Domain) - Use freely, modify freely
- **Reference Implementation:** MIT License
- **Documentation:** CC-BY-4.0

---

## 🔗 Links

- **GitHub:** https://github.com/acp0/acp0
- **Documentation:** https://github.com/acp0/acp0/tree/main/docs
- **Releases:** https://github.com/acp0/acp0/releases
- **Issues:** https://github.com/acp0/acp0/issues
- **Discussions:** https://github.com/acp0/acp0/discussions

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=acp0/acp0&type=Date)](https://star-history.com/#acp0/acp0&Date)

---

**Built with ❤️ by the ACP0 Community**

*"The future of shopping is agent-to-agent, not human-to-platform."*  
*"购物的未来是代理对代理，而非人类对平台。"*

---

## 📊 Quick Stats

- **Protocol Version:** v0.9.0
- **Tests:** 32 passing
- **Transaction Time:** 1-2 seconds
- **Lines of Code:** ~2,000 (core)
- **Languages:** Python (more coming)
- **License:** MIT

---

**Ready to build the future of commerce?** 🚀

[Get Started](#-quick-start) | [Read Docs](docs/) | [Contribute](CONTRIBUTING.md) | [Join Community](#-community)
