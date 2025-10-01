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

// AI改写提示词
const REWRITE_PROMPT = `你是一个技术文档专家。请将以下技术文章改写为10-15个简洁的问答对，适合AI爬虫和快速查询。

要求：
1. 保留原文的frontmatter（title, description等）
2. 生成10-15个问答对
3. 每个问题以"?"结尾
4. 每个答案2-3句话（50-100字）
5. 保留所有关键技术参数和数据
6. 使用Markdown格式
7. 问题要覆盖文章的主要内容点
8. 答案要简洁直接，突出重点

输出格式：
---
title: "[简化的标题]"
description: "[简短描述]"
category: "[分类]"
---

# [简化的标题]

## [问题1]?

[答案1，2-3句话，50-100字]

## [问题2]?

[答案2，2-3句话，50-100字]

## [问题3]?

[答案3，2-3句话，50-100字]

...（共10-15个问答）

请改写以下内容：`;

// 解析frontmatter
function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return { frontmatter: {}, content: content };
  
  const frontmatterText = match[1];
  const frontmatter = {};
  
  const lines = frontmatterText.split('\n');
  let currentKey = null;
  let currentValue = '';
  
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0 && !line.startsWith(' ')) {
      // 保存上一个键值对
      if (currentKey) {
        frontmatter[currentKey] = currentValue.trim().replace(/^["']|["']$/g, '');
      }
      // 开始新的键值对
      currentKey = line.substring(0, colonIndex).trim();
      currentValue = line.substring(colonIndex + 1).trim();
    } else if (currentKey) {
      // 多行值
      currentValue += ' ' + line.trim();
    }
  }
  
  // 保存最后一个键值对
  if (currentKey) {
    frontmatter[currentKey] = currentValue.trim().replace(/^["']|["']$/g, '');
  }
  
  return {
    frontmatter,
    content: content.substring(match[0].length).trim()
  };
}

// 改写单个FAQ文件
async function rewriteFAQ(faqPath) {
  try {
    console.log(`\n📝 Processing: ${path.basename(faqPath)}`);
    
    // 读取原文件
    const content = await fs.readFile(faqPath, 'utf-8');
    const { frontmatter } = parseFrontmatter(content);
    
    console.log(`   Title: ${frontmatter.title || 'Unknown'}`);
    
    // 调用OpenAI API改写
    console.log(`   🤖 Calling OpenAI API...`);
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: REWRITE_PROMPT },
        { role: 'user', content: content }
      ],
      temperature: 0.7,
      max_tokens: 2000
    });
    
    const rewrittenContent = response.choices[0].message.content;
    
    // 计算问答数量
    const qaCount = (rewrittenContent.match(/^## .+\?$/gm) || []).length;
    console.log(`   ✅ Generated ${qaCount} Q&A pairs`);
    
    // 确定输出路径
    const relativePath = path.relative(path.join(__dirname, '../faq'), faqPath);
    const outputPath = path.join(__dirname, '../ai-faq', relativePath);
    
    // 创建目录
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    
    // 写入文件
    await fs.writeFile(outputPath, rewrittenContent, 'utf-8');
    console.log(`   ✅ Saved to: ai-faq/${relativePath}`);
    
    return { success: true, qaCount };
    
  } catch (error) {
    console.error(`   ❌ Error: ${error.message}`);
    return { success: false, error: error.message };
  }
}

// 递归扫描目录
async function scanDirectory(dir) {
  const files = [];
  
  try {
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
  } catch (error) {
    console.error(`Error scanning ${dir}: ${error.message}`);
  }
  
  return files;
}

// 主函数
async function main() {
  console.log('🚀 Starting FAQ rewrite...\n');
  
  // 扫描FAQ目录
  const faqDir = path.join(__dirname, '../faq');
  console.log('📂 Scanning FAQ directory...');
  const files = await scanDirectory(faqDir);
  
  // 过滤掉README文件
  const faqFiles = files.filter(f => !f.endsWith('README.md'));
  console.log(`   ✅ Found ${faqFiles.length} FAQ files\n`);
  
  // 处理单个文件还是全部
  const targetFile = process.argv[2];
  let filesToProcess = [];
  
  if (targetFile) {
    const fullPath = path.resolve(targetFile);
    if (faqFiles.includes(fullPath)) {
      filesToProcess = [fullPath];
      console.log('📝 Processing single file mode\n');
    } else {
      console.log(`❌ File not found: ${targetFile}`);
      return;
    }
  } else {
    filesToProcess = faqFiles;
    console.log('📝 Processing all files mode\n');
  }
  
  // 批量处理
  let successCount = 0;
  let errorCount = 0;
  let totalQA = 0;
  
  for (const file of filesToProcess) {
    const result = await rewriteFAQ(file);
    if (result.success) {
      successCount++;
      totalQA += result.qaCount || 0;
    } else {
      errorCount++;
    }
    
    // 避免API限流
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // 总结
  console.log('\n' + '='.repeat(50));
  console.log(`✅ Successfully rewritten: ${successCount} files`);
  console.log(`📊 Total Q&A pairs generated: ${totalQA}`);
  if (errorCount > 0) {
    console.log(`❌ Failed: ${errorCount} files`);
  }
  console.log('='.repeat(50));
}

// 运行
main().catch(console.error);

