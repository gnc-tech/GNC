# FAQ Generation System (SEO Optimized)

双格式FAQ自动生成系统，现已集成SEO优化策略。

## 使用方法

```bash
# 生成1条FAQ（默认）
auggie --quiet write-faq

# 生成3条FAQ
auggie --quiet write-faq 3

# 生成5条FAQ（最大）
auggie --quiet write-faq 5
```

## 🎯 SEO优化更新 (2025-01-24)

### 新增15个SEO优化任务
针对核心关键词优化，优先级 10.0-7.2：
- **GNC总览** (支柱页) - `guidance navigation and control`
- **光纤陀螺仪** (5个任务) - `fiber optic gyroscope`, `FOG`
- **光学陀螺仪** - `optical gyroscope`
- **导引系统** (3个任务) - `guidance systems`
- **导航系统** (3个任务) - `navigation systems`
- **控制系统** - `control systems`
- **应用场景** (2个任务) - UAV, 导弹

### SEO配置 (config.json)
新增 `seoOptimization` 配置节：
- 核心关键词列表
- 标题格式规范
- 首段要求（必须包含品牌+GNC+关键词）
- 标题优化（H2/H3必须包含关键词）
- 内链策略（最少3-5个链接）
- 长尾关键词策略

### 详细SEO策略
查看 `SEO-STRATEGY.md` 了解：
- 当前SEO问题诊断
- 分阶段执行计划
- 预期效果和时间线
- 监控指标

## 工作流程

1. 从 `tasks.json` 选择任务（优先高priority）
2. 生成长FAQ → `faq/{category}/{filename}.md`（应用SEO优化）
3. 生成短问答 → `ai-faq/{category}/{filename}.md`（问题匹配搜索查询）
4. 更新 `completed.json`
5. Git提交并推送

## 文件说明

- **tasks.json** - 待完成任务列表（25个任务，15个新增SEO优化）
- **completed.json** - 已完成任务记录
- **config.json** - 系统配置（含SEO优化设置）
- **SEO-STRATEGY.md** - SEO优化策略文档（新增）

## 格式对比

### 长FAQ (faq/)
- 完整frontmatter（10+字段）
- 800-2500字
- 详细章节、表格、规格
- 面向传统搜索引擎

### 短问答 (ai-faq/)
- 简化frontmatter（3字段）
- 10-15个问答对
- 每个答案2-4句话
- 面向AI搜索引擎

## 任务管理

### 添加新任务

编辑 `tasks.json`，添加：

```json
{
  "id": "faq-2024-XXX",
  "topic": "任务主题",
  "category": "general|navigation|control|guidance|applications|technical",
  "priority": 9.0,
  "filename": "filename.md"
}
```

### 查看完成状态

查看 `completed.json` 中的 `metadata.totalCompleted`。

## 注意事项

- 默认生成1条，最多5条
- 自动检查重复（通过completed.json）
- 完成后自动提交Git
- 无需用户交互

## HTML实体转义规则

为避免TypeScript语法错误，生成的FAQ内容会自动转义HTML特殊字符：

### 自动转义的字符
- `<` → `&lt;` （小于号）
- `>` → `&gt;` （大于号）
- `&` → `&amp;` （和号）
- `"` → `&quot;` （双引号）
- `'` → `&#039;` （单引号）

### 常见场景示例

**技术规格中的小于号：**
```
原文：bias stability <0.01°/h
生成：bias stability &lt;0.01°/h
```

**范围表达式：**
```
原文：from <1,000 to >10,000 counts
生成：from &lt;1,000 to &gt;10,000 counts
```

**括号中的比较：**
```
原文：compact construction (<30 g)
生成：compact construction (&lt;30 g)
```

### 实现位置

转义功能已在以下脚本中实现：

1. **FAQ生成脚本** - `ai-gnc-tech/scripts/convert-faq.js`
   - `escapeHtml()` 函数自动转义所有问题和答案内容
   - 在生成Astro页面时自动应用

2. **产品页面生成脚本** - `ai-gnc-tech/scripts/rewrite-products-template.js`
   - `escapeHtml()` 函数转义产品特性、应用场景和规格表数据
   - 防止产品页面中的技术参数引起语法错误

### 为什么需要转义？

在Astro/JSX文件中，`<` 和 `>` 会被解析器识别为HTML标签的开始和结束。如果在文本内容中直接使用这些字符（如技术规格 `<0.01°/h`），会导致：

- ❌ TypeScript语法错误：`Identifier expected`
- ❌ HTML解析错误：浏览器无法正确渲染
- ❌ 构建失败：Astro编译器报错

通过自动转义，确保所有生成的内容都符合HTML规范，避免手动修复。

