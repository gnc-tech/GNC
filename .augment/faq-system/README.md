# FAQ Generation System

双格式FAQ自动生成系统。

## 使用方法

```bash
# 生成1条FAQ（默认）
auggie --quiet write-faq

# 生成3条FAQ
auggie --quiet write-faq 3

# 生成5条FAQ（最大）
auggie --quiet write-faq 5
```

## 工作流程

1. 从 `tasks.json` 选择任务
2. 生成长FAQ → `faq/{category}/{filename}.md`
3. 生成短问答 → `ai-faq/{category}/{filename}.md`
4. 更新 `completed.json`
5. Git提交并推送

## 文件说明

- **tasks.json** - 待完成任务列表
- **completed.json** - 已完成任务记录
- **config.json** - 系统配置

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

