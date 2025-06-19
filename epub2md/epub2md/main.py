#!/usr/bin/env python3
"""
epub2md - 将EPUB电子书转换为Markdown格式

命令行入口
"""

import os
import sys
import click
from . import __version__
from .epub_parser import EPUBParser
from .converter import HTMLToMarkdownConverter
from .output import OutputGenerator

@click.command()
@click.version_option(version=__version__)
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='输出目录或文件名')
@click.option('--single-file', is_flag=True, help='输出为单个Markdown文件')
@click.option('--toc/--no-toc', default=True, help='是否包含目录')
@click.option('-v', '--verbose', is_flag=True, help='显示详细信息')
def main(input_file, output, single_file, toc, verbose):
    """将EPUB电子书转换为Markdown格式"""
    try:
        # 如果没有指定输出路径，使用输入文件名作为基础
        if not output:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            if single_file:
                output = f"{base_name}.md"
            else:
                output = base_name
        
        if verbose:
            click.echo(f"正在处理: {input_file}")
            click.echo(f"输出位置: {output}")
            click.echo(f"输出模式: {'单文件' if single_file else '多文件'}")
        
        # 解析EPUB文件
        parser = EPUBParser(input_file, verbose)
        book = parser.parse()
        
        # 转换为Markdown
        converter = HTMLToMarkdownConverter(book, verbose)
        result = converter.convert()
        
        # 生成输出
        generator = OutputGenerator(result, output, single_file, toc, verbose)
        generator.generate()
        
        if verbose:
            click.echo("转换完成!")
        
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
