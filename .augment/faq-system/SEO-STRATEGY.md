# GNC Tech FAQ SEO Optimization Strategy

## 问题诊断 (Current Issues)

### 1. 搜索表现分析
- ✅ **品牌词搜索**: `gnc tech` → 第2-3页（可接受）
- ❌ **核心关键词**: `guidance`, `navigation`, `control` → 找不到
- ❌ **产品关键词**: `fiber optic gyroscope`, `optical gyroscope` → 找不到
- ❌ **组合搜索**: `gnc tech + guidance navigation control` → 不出现

### 2. 根本原因
1. **关键词覆盖不足**: 缺少针对核心词的内容
2. **技术SEO问题**: 页面标题显示为 `resources.seo.title`（i18n key未渲染）
3. **内容结构问题**: 缺少"支柱页"(pillar page)建立主题权威
4. **内链不足**: FAQ之间、FAQ与产品页之间缺少链接

## 解决方案 (Solution)

### 阶段一: 内容优化 (通过 `/write-faq` 命令)

#### 1. 创建支柱页 (Pillar Page)
**任务**: `faq-2025-seo-001` - GNC系统总览
- **目标**: 成为站点关于 GNC 的权威页面
- **关键词**: `guidance navigation and control`, `GNC systems`, `GNC`
- **内容**: 2500字，覆盖 guidance/navigation/control 三大子系统
- **链接**: 链接到所有细分FAQ和产品页

#### 2. 核心产品关键词页面
**Fiber Optic Gyroscope 系列** (5篇):
- `faq-2025-seo-002`: FOG工作原理
- `faq-2025-seo-003`: FOG vs MEMS对比
- `faq-2025-seo-005`: FOG选型指南
- `faq-2025-seo-010`: FOG技术规格
- `faq-2025-seo-015`: FOG光学组件

**Optical Gyroscope**:
- `faq-2025-seo-004`: 光学陀螺仪类型和应用

**Guidance Systems**:
- `faq-2025-seo-006`: 导弹和无人机导引系统
- `faq-2025-seo-009`: 光学导引传感器对比
- `faq-2025-seo-014`: 激光精确导引

**Navigation Systems**:
- `faq-2025-seo-007`: 航空航天导航系统
- `faq-2025-seo-011`: 惯性导航系统

**Control Systems**:
- `faq-2025-seo-008`: GNC控制系统

#### 3. 应用场景页面
- `faq-2025-seo-012`: UAV的GNC系统
- `faq-2025-seo-011`: 导弹导航系统

### 阶段二: 技术SEO修复 (需要前端配合)

#### 必须修复的问题:
1. **页面标题**: 修复 `resources.seo.title` → `Guidance, Navigation and Control Resources | GNC Tech`
2. **类别页标题**:
   - Navigation: `Navigation Systems – Fiber Optic Gyroscopes and IMUs | GNC Tech`
   - Guidance: `Guidance Systems – Sensors and Detectors | GNC Tech`
   - Control: `Control Systems – Servo Actuators and Batteries | GNC Tech`
3. **Meta描述**: 确保所有页面有正确的meta description
4. **Open Graph**: 确保社交分享标签正确

### 阶段三: 内链策略

#### 内链规则:
1. **支柱页** → 链接到所有细分FAQ
2. **细分FAQ** → 链接回支柱页 + 相关FAQ + 产品页
3. **产品页** → 链接到相关FAQ
4. **类别页** → 链接到该类别的重点FAQ

#### 示例内链结构:
```
GNC系统总览 (支柱页)
├── Guidance Systems
│   ├── 导弹导引系统 FAQ
│   ├── 光学传感器对比 FAQ
│   └── 产品: CMOS传感器
├── Navigation Systems
│   ├── FOG工作原理 FAQ
│   ├── FOG vs MEMS FAQ
│   ├── 光学陀螺仪 FAQ
│   └── 产品: FOG系列
└── Control Systems
    ├── 控制系统 FAQ
    └── 产品: 伺服执行器
```

## 执行计划 (Action Plan)

### Week 1-2: 生成核心内容
```bash
/write-faq 5  # 生成前5个高优先级任务
```
重点: GNC总览 + FOG核心页面

### Week 3-4: 生成对比和选型内容
```bash
/write-faq 5  # 生成第6-10个任务
```
重点: 对比文章 + 选型指南

### Week 5-6: 生成应用场景内容
```bash
/write-faq 5  # 生成第11-15个任务
```
重点: 应用场景 + 技术深度文章

### Week 7: 技术SEO修复
- 修复页面标题问题
- 检查所有meta标签
- 确保内链正确

### Week 8: 提交搜索引擎
- 提交sitemap到Google Search Console
- 提交sitemap到Bing Webmaster Tools
- 请求重新抓取关键页面

## 预期效果 (Expected Results)

### 3个月后:
- ✅ 长尾词排名进入前10: `fiber optic gyroscope for navigation`, `FOG vs MEMS`, `guidance systems for missiles`
- ✅ 品牌+产品词排名提升: `gnc tech fiber optic gyroscope`

### 6个月后:
- ✅ 核心产品词进入前20: `fiber optic gyroscope`, `optical gyroscope`
- ✅ 组合词进入前10: `guidance navigation and control system`

### 12个月后:
- ✅ 建立GNC领域权威，核心词进入前10
- ✅ 自然流量增长3-5倍

## 监控指标 (KPIs)

### 每月检查:
1. Google Search Console - 关键词排名变化
2. 自然流量增长
3. 页面收录数量
4. 平均排名位置
5. 点击率 (CTR)

### 重点监控关键词:
- `guidance navigation and control`
- `fiber optic gyroscope`
- `optical gyroscope`
- `FOG navigation`
- `MEMS vs FOG`
- `guidance systems`
- `navigation systems`
- `GNC systems`

