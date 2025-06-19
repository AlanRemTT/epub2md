#!/usr/bin/env python3
"""
epub2md - EPUB到Markdown转换工具
"""

from setuptools import setup, find_packages
import os
import re

# 读取版本信息
with open(os.path.join('epub2md', '__init__.py'), 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.1.0'  # 默认版本

# 读取长描述
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='epub2md',
    version=version,
    description='将EPUB电子书转换为Markdown格式',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/epub2md',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'epub2md=epub2md.main:main',
        ],
    },
    install_requires=[
        'ebooklib>=0.17.1',
        'beautifulsoup4>=4.9.0',
        'html2text>=2020.1.16',
        'Pillow>=7.0.0',
        'click>=7.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
    keywords='epub, markdown, ebook, converter',
)
