# TANCE / 摊策：AI 工程纪律

适用于本仓库全部代码。技术事实以 `docs/specs/` 为准；本文件只定义开工纪律与阅读入口。

## 每次修改代码前

1. 阅读本文件，以及 [项目边界](docs/specs/00-project-scope.md)、[开发规则](docs/specs/07-development-rules.md)。
2. 按任务阅读下表中全部适用 spec；先列出受影响模块、FROZEN contract 和验收条件，再动代码。
3. 检查 spec 的“待批准”条目。缺失、冲突和待批准提案不是自行发挥的授权。

| 修改范围 | 必读规范 |
|---|---|
| 依赖、配置、目录、数据库连接 | [01 技术栈](docs/specs/01-tech-stack.md)、[02 架构](docs/specs/02-architecture.md) |
| Model、字段、FK、索引、migration | [03 数据模型](docs/specs/03-data-model.md)、[05 状态规则](docs/specs/05-state-rules.md) |
| Router、Pydantic、对外响应 | [04 API](docs/specs/04-api-contract.md)、[05 状态规则](docs/specs/05-state-rules.md)、[06 Service](docs/specs/06-service-contracts.md) |
| 业务、库存、销售、推荐、AI | [03 数据模型](docs/specs/03-data-model.md)、[04 API](docs/specs/04-api-contract.md)、[05 状态规则](docs/specs/05-state-rules.md)、[06 Service](docs/specs/06-service-contracts.md) |
| 重大架构决策、已批准规范变更 | [ADR 使用规则](docs/specs/decisions/README.md) |

## 不可越过的边界

- **Implementation must conform to specification. Specification must not conform to implementation.**
- **Do not change a FROZEN contract to make implementation easier.** 字段、类型、关系、状态、API、计算语义、AI 边界均不可擅改。
- FROZEN / SEMI-FROZEN / FLEXIBLE 的判定见 07。迁移工具、测试通过、开发方便都不构成修改 FROZEN contract 的授权。
- 如发现 spec 有问题、冲突、缺项，或实现必须改变冻结约定，**立即停止受影响实现**，输出下述内容；等待用户明确批准后，先改 spec，再改 migration、代码、测试。无关且已授权工作可以继续。

```text
SPEC CHANGE REQUIRED
Affected spec: <文件 / 章节 / 规则编号>
Current rule: <现行约定；若缺项则明确写未定义>
Problem: <具体冲突、反例或无法实现之处>
Proposed change: <可审阅的新规则>
Impact: <API / schema / migration / 状态 / 测试 / 兼容性>
```

- 不引入未经批准的依赖或架构层；同步 SQLAlchemy；Schema 由 Alembic 管理，禁止用 `create_all()` 代替 migration。
- Python 负责数值推荐，LLM 仅解释；LLM 失败仍应返回并保存有效数值结果。
- 不增加库存余额、历史销量、OVERDUE 等重复存储；不混淆数量建议、生产下单、实际到货、库存预留和销量。
- 只实现当前任务最小范围，不扩前端 UI、用户鉴权、后台队列或其他 V2 功能。

## 交付报告

完成任务后必须报告：

```text
files changed: <文件及用途>
tests run: <实际执行内容、结果；未执行则写原因>
spec impact: <无变更 / 已批准变更及批准依据 / 待解决冲突>
```

不得声称未运行的测试通过；不得把待批准提案当成已冻结规则。
