<div align="center">
  <h1>🕊️ 数字遗产管家 · DigitalLegacy</h1>
  <p><strong>一站式数字资产管理与情感传承工具</strong></p>
  <p>解决"人在意外发生后，数字信息无法触达家属"以及"隐私信息如何安全托付"的痛点</p>
</div>

---

## 📖 项目简介

**数字遗产管家** 是一个帮助用户系统性管理数字资产、并在适当时机安全传递给受益人的全栈 Web 应用。

现代人平均拥有超过 10 个在线账号，关键数字资产信息仅存储于个人大脑或手机笔记中，缺乏系统性管理，超过 70% 的人未对数字遗产做任何安排。本产品旨在解决这一空白。

### 核心痛点

- ❌ 家人因不知密码，无法继承虚拟货币、证券账号、在线订阅等数字资产
- ❌ 逝者社交动态被误用，私密照片与聊天记录面临被公开的风险
- ❌ 临终嘱托、告别信无法在精准的时间点传达给亲人

---

## ✨ 功能模块

### 🔐 保险箱 (The Vault)

分类管理用户的所有数字资产，支持加密存储：

| 分类 | 说明 |
|------|------|
| 银行/理财 | 银行账户、理财平台、证券账号 |
| 加密货币 | 私钥、助记词分段存储 |
| 保险保单 | 保单扫描件、保险信息 |
| 社交媒体 | 微信、微博、Twitter 等账号密码 |
| 邮箱 | 各邮箱账号及密码 |
| 云服务 | iCloud、Google Drive、OneDrive 等 |
| 关键指令 | 葬礼偏好、宠物安置、文件销毁指令 |

### 💌 情感档案 (Emotional Files)

为用户提供情感留存空间，可指定受益人：
- 📝 **信件** — 给亲人的最后一封信
- 🎤 **语音** — 预录语音留言
- 🎬 **视频** — 预录视频遗言
- 支持指定特定受益人查看，触发后才可解密

### 👨‍👩‍👧 受益人管理 (Beneficiaries)

- 邀请家人或好友成为受益人
- **实名认证** — 通过身份证号核验身份
- **三级权限分配** — 保险箱 / 情感档案 / 密钥分片 独立授权
- **盲信机制** — 触发前受益人仅知自己被列为受益人，无法查看内容

### 🛡️ 生命开关 (Dead Man's Switch)

**这是产品的灵魂功能**，采用阶梯式预警触发机制：

```
T+0 天 → App 强提醒推送
T+3 天 → 短信 + 自动语音电话
T+7 天 → 联系一级安全联系人核实
最终   → 向受益人发送解锁链接/密钥
```

用户只需定期"安全打卡"即可维持守护状态。支持**一键紧急撤回**。

### ⚙️ 安全设置 (Security)

- **零知识加密** — AES-256 加密存储，开发者也无法查看用户内容
- **多因子认证 (MFA)** — 生物识别 + 传统密码
- **密钥分片** — 重要私钥拆分为两部分，一部分 APP 存储，一部分物理保管
- **紧急联系人** — 设置 T+7 天的核实联系人

---

## 🏗️ 技术栈

| 层级 | 技术 |
|------|------|
| **前端** | Vue 3 + TypeScript + Vite |
| **UI 框架** | Element Plus（国际化中文） |
| **状态管理** | Pinia |
| **路由** | Vue Router 4 |
| **后端** | Python FastAPI (异步) |
| **数据库** | SQLAlchemy 2.0 + SQLite (支持切换 PostgreSQL) |
| **认证** | JWT + bcrypt |
| **加密** | Fernet (AES-256) |

---

## 🚀 快速启动

### 前置要求

- Python 3.10+
- Node.js 18+

### 1. 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端运行在 `http://localhost:8000`，API 文档访问 `http://localhost:8000/docs`

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 `http://localhost:5173`

### 3. 一键启动

```bash
bash start.sh
```

---

## 📂 项目结构

```
DigitalLegacy/
├── backend/
│   └── app/
│       ├── api/          # RESTful API 路由
│       │   ├── auth.py           # 注册/登录/MFA
│       │   ├── vault.py          # 保险箱 CRUD
│       │   ├── emotional.py      # 情感档案 CRUD
│       │   ├── beneficiaries.py  # 受益人管理
│       │   └── trigger.py        # 生命开关核心逻辑
│       ├── models/       # SQLAlchemy 数据模型
│       ├── schemas/      # Pydantic 请求/响应校验
│       ├── core/         # 加密、JWT、依赖注入
│       └── main.py       # 应用入口
├── frontend/
│   └── src/
│       ├── api/          # Axios API 客户端
│       ├── views/        # 页面组件
│       ├── stores/       # Pinia 状态管理
│       └── router/       # 路由配置
└── start.sh              # 一键启动脚本
```

---

## 🧪 API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/register` | 用户注册 |
| POST | `/auth/login` | 用户登录 |
| GET | `/auth/me` | 获取当前用户 |
| GET/POST | `/vault/` | 保险箱列表/创建 |
| GET/PUT/DELETE | `/vault/{id}` | 保险箱详情/更新/删除 |
| GET/POST | `/emotional/` | 情感档案列表/创建 |
| GET/POST | `/beneficiaries/` | 受益人列表/创建 |
| POST | `/beneficiaries/{id}/verify` | 受益人实名认证 |
| GET/PUT | `/trigger/config` | 生命开关配置 |
| POST | `/trigger/check-in` | 安全打卡 |
| GET | `/trigger/status` | 触发状态查询 |
| POST | `/trigger/emergency-recall` | 紧急撤回 |

---

## 📜 开源协议

MIT License

---

<div align="center">
  <p>用代码守护爱与记忆 🕊️</p>
</div>
