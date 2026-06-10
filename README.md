# Targeted Company Research Skill

`targeted-company-research` 是一个面向企业定向调研的公开 skill。它把一个目标公司拆成 5 条证据链：公司基本面、产品技术、行业竞品、客户渠道供应链、营销事件与 ABM 切入点，最终输出带来源标注的本地 Markdown 报告。

## 核心策略价值

企业调研的价值不在于“搜到几段公司简介”，而在于把目标公司变成一张可验证的业务地图：

- 销售团队知道目标客户是谁、卖什么、向谁卖、在哪些渠道出现、该从什么话题切入。
- 市场团队知道目标公司的定位、内容、展会、渠道和竞品对比。
- 合作伙伴团队能区分已证实事实、第三方估算和信息缺口。
- 竞品研究团队能把产品、技术、渠道、客户和市场位置放进同一份报告。
- 管理层拿到的是有来源、有置信度、有缺口说明的判断，而不是泛泛的公司介绍。

## 适用场景

- B2B 销售前期客户调研。
- ABM 大客户营销准备。
- 竞品、合作伙伴、供应商、渠道商调研。
- 投资、并购、代理合作前的轻量尽调。
- 对一个海外公司、本土公司、品牌、子公司或目标客户做深度画像。

## Skill 会产出什么

默认产出本地项目目录：

```text
projects/{project_slug}/
├── task_plan.md
├── task_status.md
├── task1_company/task_instructions.md
├── task1_company/task1_company.md
├── task2_product/task_instructions.md
├── task2_product/task2_product.md
├── task3_industry/task_instructions.md
├── task3_industry/task3_industry.md
├── task4_channel/task_instructions.md
├── task4_channel/task4_channel.md
├── task5_marketing/task_instructions.md
├── task5_marketing/task5_marketing.md
├── sources/source_index.md
├── evidence/
└── FINAL_REPORT.md
```

`FINAL_REPORT.md` 默认包含：

- 公司基本面、历史、股权、管理层、规模、合规。
- 产品线、技术规格、认证、价格与评价信号。
- 行业规模、竞品矩阵、竞争定位、机会与风险。
- 客户、渠道、分销商、供应链、采购信号。
- 营销内容、展会活动、公开业务决策人、ABM 切入建议。
- 信息缺口和来源索引。
- 附录保留 5 个子任务完整报告，主报告保留汇总判断。

## 检索策略

Skill 要求智能体同时使用三类能力：

- `web_search`：发现来源、拓展关键词、找别名、子公司、产品型号、竞品、渠道和人物。
- `web_fetch`：提取官网、PDF、产品页、监管文件、新闻稿、协会页、展会页、市场资料。
- 浏览器/CDP：处理 JavaScript 渲染页面、公开电商页、展会目录、认证查询页、公开 profile 页面，以及用户已授权的真实浏览器会话。

来源优先级：

- T0：监管文件、法院记录、海关/进出口、专利、认证数据库、官方注册信息。
- T1：官网、官方 PDF、产品文档、新闻稿、投资者页面、官方社媒。
- T2：行业协会、展会、分销商、市场平台、可信媒体。
- T3：第三方估算、线索数据库、评论聚合页，只能标注为估算。

## 安装到 Codex

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo AAAAAAlone/targeted-company-research-skill \
  --path targeted-company-research \
  --method git
```

安装后重启 Codex。

## Codex 使用示例

```text
Use $targeted-company-research to research Universal Power Group for ABM sales preparation. Output in Chinese. Focus on products, distributors, competitors and public decision makers.
```

```text
Use $targeted-company-research to research {公司名}. 重点看产品线、渠道、竞品和 ABM 切入点，输出中文 Markdown 报告，保留来源标注和数据缺口。
```

## 龙虾 OpenClaw 或其他智能体使用方式

把 `targeted-company-research/` 目录复制到对应智能体的 skills 目录，或者让智能体直接读取：

```text
targeted-company-research/SKILL.md
```

智能体需要具备等价能力：

- Web search。
- 网页/PDF fetch。
- 本地文件写入。
- 可选浏览器/CDP 访问。
- 可选多 worker/子任务并行。

没有多 worker 能力也可以使用：按 5 个任务顺序执行，再合并成 `FINAL_REPORT.md`。

Codex 默认建议顺序执行：Task 1 到 Task 5 逐个完成，每完成一个任务更新 `task_status.md`。多 worker 只作为加速选项，不是必需条件。

## 数据边界

这个 skill 只支持合法的公开商业调研和用户授权会话。

允许收集：

- 公开业务姓名。
- 职位、公司、公开 profile URL。
- 公开演讲、展会、新闻稿、协会页面。
- 官方联系方式、官方表单、公开公司邮箱。

不支持：

- 绕过登录、付费墙、验证码或访问控制。
- 提取私密系统数据。
- 猜测私人邮箱或手机号。
- 批量收集个人联系方式。
- 使用泄露凭证、cookie 或 token。

## 仓库结构

```text
targeted-company-research/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── research-playbook.md
    └── task-instructions-template.md
```

## License

MIT License.
