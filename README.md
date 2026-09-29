# TANCE（摊策）

基于 `TANCE_Frontend_Demo_Spec_v2.md` 实现的 Vue 3 + TypeScript 工作台，配套 FastAPI + MySQL V1 后端。默认使用本地 Mock，开启 API 数据模式后会读取并持久化商品、展会、参展计划、需求信号、数量建议、生产、库存分配、销售和任务。

打开工作台后，可通过导航底部切换 8 种演示场景。新增、编辑、需求快照、备货决策、批次到货、库存分配和销售记录均可操作；刷新或切换场景会重置演示数据。详细操作见 [页面 Demo 说明](docs/页面Demo说明.md)。

## 启动

在终端进入此项目：

```bash
cd '/Users/haoduozhangdayang/Documents/ChatGPT/寒假实习求职/tance'
make dev
```

- 前端工作台：http://127.0.0.1:5173/dashboard
- 环境检查页：http://127.0.0.1:5173/environment
- FastAPI 交互式 API 文档：http://127.0.0.1:8000/docs
- 后端存活检查：http://127.0.0.1:8000/api/health
- 后端与数据库检查：http://127.0.0.1:8000/api/health/ready

`Ctrl+C` 同时停止本次启动的前后端。启动脚本遇到 5173 / 8000 端口占用时会说明原因，不会终止其他项目。

MySQL 已通过 Homebrew 注册为本机登录服务，前后端停止后数据库仍会运行。

```bash
make db-start  # 启动 MySQL
make db-stop   # 不开发时可停止 MySQL
```

## 常用命令

```bash
make doctor   # 检查 Python、依赖、开发库和测试库连接
make test     # pytest：API、错误响应、真实 MySQL 集成检查
make build    # TypeScript 检查与 Vite 生产构建
make migrate  # 执行已审阅的 Alembic V1 迁移
make db-shell # 通过本地受保护的配置文件进入 MySQL 管理终端
```

前端业务边界检查：在 `frontend` 目录执行 `npm run check:demo`，验证需求快照、建议历史、到货入库、库存分配与销售数量约束。

分别启动前后端：

```bash
# 终端 1，在项目根目录
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 终端 2，在项目根目录
cd frontend
npm run dev
```

前端 `/api` 请求由 Vite 转发到 `127.0.0.1:8000`。Axios 默认将业务请求发送到 `/api/v1`，健康检查仍使用 `/api/health/ready`。后端 CORS 允许本机前端地址。

### 启用真实 API 数据

在 `frontend/.env.local` 写入以下配置，然后重启 Vite：

```dotenv
VITE_WORKSPACE_SOURCE=api
VITE_API_BASE_URL=/api/v1
```

页面右上角显示 `API` 时，列表会由后端加载，支持的表单保存会写入 MySQL；未设置该开关时保留可重复演示的 Mock 场景。

### 在线演示

推送到 GitHub 后，`.github/workflows/deploy-pages.yml` 会自动发布静态演示到 GitHub Pages。线上版本刻意使用 Mock 数据，因此无需公开数据库密码或运行中的后端；完整 API 模式请按上文在本机启动 MySQL 与 FastAPI。

## 运行环境与目录

- Node.js：沿用本机 22.18.0；版本提示保存在 `.node-version`。
- Python：Homebrew Python 3.13，后端使用 `backend/.venv`，不修改 macOS 自带 Python。
- MySQL：Homebrew `mysql@8.4`，只监听本机回环地址。
- 开发库：`tance_dev`；测试库：`tance_test`；字符集 `utf8mb4`。
- 应用账户：`tance@localhost`，权限限于上述两个数据库。
- `frontend/package-lock.json` 和 `backend/requirements.txt` 锁定本次验证的依赖版本。
- VS Code：直接打开此 `tance` 文件夹，会读取 `.vscode` 中的解释器、pytest 与插件建议。

```text
tance/
├── frontend/          Vue 页面、Router、Pinia、Mock/API 数据源与环境检查页
├── backend/
│   ├── app/api/       HTTP 路由
│   ├── app/models/    SQLAlchemy V1 领域模型
│   ├── app/schemas/   Pydantic API 类型
│   ├── app/services/  确定性业务服务与状态校验
│   ├── app/ai/        可替换 LLM 解释层
│   ├── app/db/        数据库引擎、Session、Base
│   ├── alembic/       已审阅的 V1 迁移
│   └── tests/         API、迁移与 MySQL 集成测试
├── scripts/           启动、自检、数据库初始化
├── docs/              Demo 使用说明与环境检查记录
├── .env.example       无密钥的配置模板
└── .env               本机配置，Git 忽略，权限 0600
```

## 密钥与 LLM

本机 `.env` 保存随机生成的数据库密码。MySQL 管理员密码保存在 `.secrets/mysql-admin.cnf`，仅用于管理终端；应用不使用 root。两者均被 Git 忽略，文件权限为 0600，不要复制到前端或上传仓库。

LLM 默认关闭。选好服务商后在根目录 `.env` 填写：

```dotenv
LLM_ENABLED=true
LLM_PROVIDER=your_provider
LLM_BASE_URL=https://your-provider.example/api
LLM_MODEL=your_model
LLM_API_KEY=your_private_key
```

以上仅为配置接口，LLM 请求适配器和业务解释功能尚未实现；环境自检不会调用付费 API。前端 `VITE_*` 变量会打包进浏览器，不能保存任何密钥。

## 在另一台机器复现

```bash
brew install python@3.13 mysql@8.4
brew services start mysql@8.4
/opt/homebrew/bin/python3.13 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
cd frontend
npm ci
cd ..
backend/.venv/bin/python scripts/setup_database.py
make doctor
make test
make build
```

上述命令面向 Apple Silicon macOS，另需安装兼容的 Node.js（22.12+，此项目验证版本为 22.18.0）。数据库初始化脚本仅创建 `tance_dev`、`tance_test` 和本地应用账户，不清空已有数据库。只有全新、空密码 root 的安装可加 `--secure-new-root` 设置随机管理员密码。已有管理员凭据的机器应通过环境变量 `MYSQL_ADMIN_PASSWORD` 或本地受保护的管理员配置提供凭据。

## 目前边界

当前 Demo 使用自建 Vue 组件与 CSS，无额外 UI 组件库。真实 API 模式采用已实现的确定性 V1 推荐规则；LLM 仅为可替换的解释层。前端为保持既有展示，未在后端建模的视觉字段（如色调、封面简称、IP 标签）以本地展示默认值呈现。
