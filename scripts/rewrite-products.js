import OpenAI from 'openai';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { config } from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 加载环境变量
config({ path: path.join(__dirname, '../.env') });

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// 加载产品数据用于URL校验
let productsData = null;
async function loadProductsData() {
  if (!productsData) {
    const data = await fs.readFile(path.join(__dirname, '../gnc-tech.json'), 'utf-8');
    productsData = JSON.parse(data);
  }
  return productsData;
}

// 根据型号查找正确的URL
function findProductUrl(model) {
  if (!productsData) return null;
  // 尝试完整匹配
  let product = productsData.products.find(p => p.model === model);
  // 如果没找到，尝试去掉前缀匹配（如 K-JD-XZ60D200 -> XZ60D200）
  if (!product && model.includes('-')) {
    const shortModel = model.split('-').pop();
    product = productsData.products.find(p => p.model === shortModel);
  }
  return product ? product.url : null;
}

// AI改写提示词
const REWRITE_PROMPT = `你是一个技术文档专家。请将以下产品规格文档改写为AI爬虫友好的技术速查格式。

要求：
1. 添加frontmatter（title, description, keywords）
2. 开头添加"Quick Answer"段落（50-100字概述）
3. 添加"What is [产品名]?"章节
4. 保留所有技术规格表格
5. 添加"When to Use"章节（列表格式）
6. 添加"Integration Guide"章节（简化的关键参数）
7. 如果有多个型号，添加"Comparison"表格
8. 底部添加CTA链接到主站
9. 保持所有数字、型号、参数完全不变
10. 使用Markdown格式

输出格式示例：
---
title: "[型号] [产品类型] - Technical Reference"
description: "[简短描述，包含关键参数]"
keywords: "[型号], [产品类型], [关键词]"
---

# [型号] [产品类型]

> **Quick Answer**: [50-100字的产品概述，包含核心参数和应用]

## What is [型号]?

[详细介绍产品技术原理和特点，2-3段]

**Key Specifications:**
- [关键参数1]
- [关键参数2]
- [关键参数3]

## Technical Quick Reference

### Performance Specifications
[保留原始规格表格]

### When to Use [型号]?
- ✅ [使用场景1]
- ✅ [使用场景2]
- ✅ [使用场景3]

### Integration Guide
**Power Requirements:**
[关键电源参数]

**Pin Configuration:**
[简化的引脚说明]

**Mounting:**
[安装要点]

## Comparison with Alternatives
[如果有多个型号，添加对比表格]

## Related Products
- [相关产品链接]

---

📘 **Complete Documentation**: [View full specifications on gnc-tech.com →]([URL])

💬 **Technical Support**: [Contact our engineering team →](https://www.gnc-tech.com/contact)

请改写以下内容：`;

// 解析frontmatter
function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return { frontmatter: {}, content: content };
  
  const frontmatterText = match[1];
  const frontmatter = {};
  
  const lines = frontmatterText.split('\n');
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }
  
  return {
    frontmatter,
    content: content.substring(match[0].length).trim()
  };
}

// 提取产品型号
function extractModel(content) {
  const match = content.match(/\*\*Product Model\*\*\s*\|\s*`([^`]+)`/);
  return match ? match[1] : null;
}

// 改写单个产品文件
async function rewriteProduct(filePath) {
  try {
    console.log(`\n📝 Processing: ${path.basename(filePath)}`);
    
    // 读取原文件
    const content = await fs.readFile(filePath, 'utf-8');
    const { frontmatter, content: markdown } = parseFrontmatter(content);
    
    // 提取型号
    const model = extractModel(content);
    console.log(`   Model: ${model || 'Unknown'}`);
    
    // 调用OpenAI API改写
    console.log(`   🤖 Calling OpenAI API...`);
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: REWRITE_PROMPT },
        { role: 'user', content: content }
      ],
      temperature: 0.7,
      max_tokens: 3000
    });
    
    let rewrittenContent = response.choices[0].message.content;
    
    // 校验并修正URL
    if (model) {
      const correctUrl = findProductUrl(model);
      if (correctUrl) {
        console.log(`   ✅ URL verified: ${correctUrl}`);
        // 替换URL占位符
        rewrittenContent = rewrittenContent.replace(/\[View full specifications on gnc-tech\.com →\]\([^\)]+\)/, 
          `[View full specifications on gnc-tech.com →](${correctUrl})`);
      } else {
        console.log(`   ⚠️  URL not found for model: ${model}`);
      }
    }
    
    // 写回文件
    await fs.writeFile(filePath, rewrittenContent, 'utf-8');
    console.log(`   ✅ Rewritten successfully`);
    
    return { success: true, model };
    
  } catch (error) {
    console.error(`   ❌ Error: ${error.message}`);
    return { success: false, error: error.message };
  }
}

// 递归扫描目录
async function scanDirectory(dir) {
  const files = [];
  const items = await fs.readdir(dir, { withFileTypes: true });
  
  for (const item of items) {
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      const subFiles = await scanDirectory(fullPath);
      files.push(...subFiles);
    } else if (item.isFile() && item.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  
  return files;
}

// 主函数
async function main() {
  console.log('🚀 Starting product rewrite...\n');
  
  // 加载产品数据
  console.log('📦 Loading product data...');
  await loadProductsData();
  console.log(`   ✅ Loaded ${productsData.products.length} products\n`);
  
  // 扫描产品目录
  const productsDir = path.join(__dirname, '../products');
  console.log('📂 Scanning products directory...');
  const files = await scanDirectory(productsDir);
  
  // 过滤掉README文件
  const productFiles = files.filter(f => !f.endsWith('README.md'));
  console.log(`   ✅ Found ${productFiles.length} product files\n`);
  
  // 处理单个文件还是全部
  const targetFile = process.argv[2];
  let filesToProcess = [];
  
  if (targetFile) {
    const fullPath = path.resolve(targetFile);
    if (productFiles.includes(fullPath)) {
      filesToProcess = [fullPath];
      console.log('📝 Processing single file mode\n');
    } else {
      console.log(`❌ File not found: ${targetFile}`);
      return;
    }
  } else {
    filesToProcess = productFiles;
    console.log('📝 Processing all files mode\n');
  }
  
  // 批量处理
  let successCount = 0;
  let errorCount = 0;
  
  for (const file of filesToProcess) {
    const result = await rewriteProduct(file);
    if (result.success) {
      successCount++;
    } else {
      errorCount++;
    }
    
    // 避免API限流
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // 总结
  console.log('\n' + '='.repeat(50));
  console.log(`✅ Successfully rewritten: ${successCount} files`);
  if (errorCount > 0) {
    console.log(`❌ Failed: ${errorCount} files`);
  }
  console.log('='.repeat(50));
}

// 运行
main().catch(console.error);

