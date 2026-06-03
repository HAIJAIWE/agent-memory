# Agent Memory System 🧠

智能体记忆系统 - 一个无限制、分层的记忆管理系统，为 AI 智能体提供强大的持久化和检索能力。

## 特性

### 核心功能
- ✨ **无限存储** - 支持几百万条记忆，无存储限制
- 🎯 **智能分层** - 微观、段级、宏观、索引四层记忆架构
- 🔍 **多维检索** - 语义搜索、关键词搜索、混合搜索、关系追踪
- ⚡ **高效缓存** - 多层缓存系统，10-100x 性能提升
- 🔄 **自动回想** - 智能体自动回想相关记忆

### 增强功能
- 🗑️ **智能去重** - 自动检测和合并重复记忆
- 📝 **自动总结** - 旧记忆自动压缩和归档
- 📌 **版本控制** - 完整的版本历史和回滚能力
- 📊 **实时监控** - 系统健康监控和性能诊断
- 💾 **灵活导出** - 支持 JSON、CSV、Markdown、完整备份

## 快速开始

### 安装

```bash
git clone https://github.com/HAIJAIWE/agent-memory.git
cd agent-memory
pip install -r requirements.txt
```

### 基本使用

```python
from src.memory_system import EnhancedMemorySystem

# 初始化记忆系统
memory = EnhancedMemorySystem()

# 存储记忆
result = memory.smart_store(
    task_type='code_gen',
    task_description='实现快速排序算法',
    original_content='',
    modified_content='def quick_sort(arr):\n    ...',
    modifications=[{
        'what': '实现快速排序',
        'before': '',
        'after': 'def quick_sort(arr):\n    ...',
        'reason': '完成用户需求'
    }]
)

# 回想相关记忆
memories = memory.smart_recall('排序算法的实现')
print(memories)
```

## 项目结构

```
agent-memory/
├── src/                          # 源代码
│   ├── models/                   # 数据模型
│   ├── database/                 # 数据库层
│   ├── vector/                   # 向量索引
│   ├── search/                   # 搜索引擎
│   ├── storage/                  # 存储引擎
│   ├── cache/                    # 缓存系统
│   ├── enhancement/              # 增强功能
│   ├── export/                   # 导出工具
│   ├── mcp/                      # MCP 工具接口
│   └── memory_system.py          # 主系统
├── tests/                        # 测试
├── examples/                     # 使用示例
├── docs/                         # 文档
└── requirements.txt              # 依赖
```

## 文档

- [架构设计](docs/ARCHITECTURE.md)
- [使用指南](docs/USAGE_GUIDE.md)
- [API 参考](docs/API_REFERENCE.md)

## 核心概念

### 记忆层级

- **微观记忆** (Micro): 几百字，单次操作、决策点
- **段级记忆** (Segment): 1-5K字，单个文件、章节
- **宏观记忆** (Macro): 10K+字，完整项目、系统
- **索引记忆** (Index): 几十字，快速导航和查询

### 搜索策略

- **语义搜索**: 基于向量的语义相似度
- **关键词搜索**: 基于 FTS5 的全文搜索
- **混合搜索**: 语义 + 关键词结合
- **关系搜索**: 基于记忆间的关联关系

## License

MIT
