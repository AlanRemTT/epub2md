# epub2md

epub2md 是一个将EPUB电子书转换为Markdown格式的命令行工具。它能保留原书籍的内容结构、图片和格式，支持单文件或多文件输出模式。

## 功能特点

- 支持将EPUB电子书转换为Markdown格式
- 保留原书籍的标题、段落、列表、加粗、斜体等格式
- 提取并保存图片资源
- 保留完整目录结构
- 支持单文件或多文件输出模式
- 支持中文等多语言内容

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
git clone https://github.com/yourusername/epub2md.git
cd epub2md
pip install -e .
```

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
