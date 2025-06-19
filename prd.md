# EPUB到Markdown转换工具开发文档

## 项目概述
开发一个命令行工具，用于将EPUB电子书格式转换为Markdown文件，保留原书籍的内容结构、图片和格式。

## 功能需求

1. 读取并解析EPUB文件
2. 提取EPUB中的文本内容、图片和目录结构
3. 将HTML内容转换为Markdown格式
4. 保留原始格式（标题、段落、列表、加粗、斜体等）
5. 提取并保存图片
6. 生成完整目录结构
7. 支持输出为单文件或多文件模式
8. 支持中文等多语言内容

## 技术选型

### 开发语言
- Python (推荐使用Python 3.8+)

### 核心依赖库
- `ebooklib`: 用于解析EPUB文件
- `BeautifulSoup4`: 用于解析HTML内容
- `html2text`: 用于将HTML转换为Markdown
- `Pillow`: 用于处理图片
- `click`: 用于构建命令行界面

## 系统架构设计

### 模块划分
1. **EPUB解析模块**: 解析EPUB文件结构和内容
2. **HTML到Markdown转换模块**: 将HTML内容转换为Markdown
3. **资源处理模块**: 处理图片等资源文件
4. **文件输出模块**: 生成最终的Markdown文件
5. **命令行界面模块**: 提供用户交互界面

### 工作流程
1. 读取EPUB文件
2. 提取元数据和目录结构
3. 遍历每个章节并转换
4. 处理和保存图片资源
5. 生成输出文件

## 开发步骤

### 1. 环境准备
```bash
# 创建项目目录
mkdir epub2md
cd epub2md

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # 在Windows上使用: venv\Scripts\activate

# 安装依赖
pip install ebooklib beautifulsoup4 html2text pillow click
```

### 2. 项目结构创建
```
epub2md/
├── epub2md/
│   ├── __init__.py
│   ├── main.py          # 主入口
│   ├── epub_parser.py   # EPUB解析器
│   ├── converter.py     # HTML到Markdown转换
│   ├── resource.py      # 资源处理
│   └── output.py        # 输出处理
├── tests/               # 测试文件
├── setup.py             # 包安装配置
├── README.md            # 项目说明
└── requirements.txt     # 依赖列表
```

### 3. 核心模块开发

#### 3.1 EPUB解析模块实现
- 创建`epub_parser.py`，实现EPUB文件的读取和解析
- 提取元数据、目录结构和内容

#### 3.2 HTML到Markdown转换模块实现
- 创建`converter.py`，实现HTML到Markdown的转换
- 处理常见HTML标签的转换规则
- 保留格式信息

#### 3.3 资源处理模块实现
- 创建`resource.py`，处理图片等资源
- 提取和保存图片文件
- 更新Markdown中的图片链接

#### 3.4 输出模块实现
- 创建`output.py`，处理输出文件的生成
- 支持单文件和多文件模式

#### 3.5 命令行界面实现
- 在`main.py`中实现命令行界面
- 设计合理的参数和选项

### 4. 测试与调试
- 编写单元测试
- 使用真实EPUB文件进行测试
- 验证转换结果的正确性

### 5. 打包和发布
- 完善`setup.py`
- 生成可安装包
- 发布到PyPI（可选）

## 具体代码实现

首先创建项目基本结构：

```bash
mkdir -p epub2md/epub2md
touch epub2md/epub2md/__init__.py
touch epub2md/setup.py
touch epub2md/requirements.txt
touch epub2md/README.md
```

接下来我们将分步骤实现各个核心模块。我会先设计各个模块的主要代码框架，然后再进行实际开发。

## 预估开发时间

| 阶段 | 预计时间 |
|------|----------|
| 环境准备和项目结构创建 | 1天 |
| 核心模块开发 | 3-4天 |
| 测试与调试 | 1-2天 |
| 打包和文档完善 | 1天 |
| 总计 | 6-8天 |

## 可能遇到的问题及解决方案

1. **复杂HTML格式转换问题**
   - 解决方案：定制html2text转换规则，处理特殊格式情况

2. **图片路径处理**
   - 解决方案：建立资源映射表，确保图片链接正确

3. **目录结构重建**
   - 解决方案：解析toc.ncx或nav.xhtml文件，重建目录结构

4. **编码问题**
   - 解决方案：统一使用UTF-8编码，处理特殊字符

5. **大型EPUB文件处理**
   - 解决方案：分块处理内容，减少内存占用

您是否需要我进一步详细说明某个部分的代码实现，或者有其他特定需求需要我考虑？