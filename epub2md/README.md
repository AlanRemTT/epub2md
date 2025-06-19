# epub2md

epub2md 是一个将EPUB电子书转换为Markdown格式的命令行工具。它能保留原书籍的内容结构、图片和格式，支持单文件或多文件输出模式。

## 功能特点

- 支持将EPUB电子书转换为Markdown格式
- 保留原书籍的标题、段落、列表、加粗、斜体等格式
- 提取并保存图片资源
- 保留完整目录结构
- 支持单文件或多文件输出模式
- 支持中文等多语言内容
- 章节间导航链接，方便阅读

## 安装

```bash
pip install epub2md
```

## 使用方法

### 基本用法

```bash
epub2md 你的电子书.epub
```

这将在当前目录中创建与电子书同名的文件夹，并生成多个Markdown文件。

### 指定输出路径

```bash
epub2md 你的电子书.epub -o 输出目录
```

### 生成单个Markdown文件

```bash
epub2md 你的电子书.epub -o 输出文件.md --single-file
```

### 不包含目录

```bash
epub2md 你的电子书.epub --no-toc
```

### 显示详细信息

```bash
epub2md 你的电子书.epub -v
```

### 帮助信息

```bash
epub2md --help
```

## 安装开发版本

如果你想安装开发版本，可以从源代码安装：

```bash
git clone https://github.com/AlanRemTT/epub2md.git
cd epub2md
pip install -e .
```

## 版本更新

### v0.1.0 (2024-06-19)
- 初始版本发布
- 支持基本的EPUB到Markdown转换功能
- 支持提取和保存图片资源
- 支持单文件和多文件输出模式

### v0.1.1 (2024-06-19)
- 改进文件命名方式，使用更有意义的章节名
- 完善目录结构，添加内部链接
- 为各章节文件添加导航链接，便于阅读
- 修复EPUB解析中的错误处理

## 依赖

- Python 3.6+
- ebooklib: 用于解析EPUB文件
- BeautifulSoup4: 用于解析HTML内容
- html2text: 用于将HTML转换为Markdown
- Pillow: 用于处理图片
- click: 用于构建命令行界面

## 贡献

欢迎提交问题和贡献代码。请确保在提交拉取请求之前，你的代码通过了所有测试。

## 许可证

本项目采用MIT许可证。 