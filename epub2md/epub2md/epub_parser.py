"""
EPUB解析模块 - 负责解析EPUB文件结构和内容
"""

import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional

class EPUBParser:
    """EPUB文件解析器"""
    
    def __init__(self, epub_path: str, verbose: bool = False):
        """
        初始化EPUB解析器
        
        Args:
            epub_path (str): EPUB文件路径
            verbose (bool): 是否显示详细信息
        """
        self.epub_path = epub_path
        self.verbose = verbose
        self.book = None  # type: Optional[epub.EpubBook]
        self.metadata = {}
        self.toc = []
        self.spine = []
        self.images = {}
        
    def parse(self) -> Dict[str, Any]:
        """
        解析EPUB文件
        
        Returns:
            dict: 包含解析后的书籍内容，结构如下:
                {
                    'metadata': {书籍元数据},
                    'toc': [目录项列表],
                    'spine': [内容顺序列表],
                    'content': {id: html内容的字典},
                    'images': {id: 图片数据的字典}
                }
        """
        if self.verbose:
            print(f"正在解析EPUB文件: {self.epub_path}")
        
        # 读取EPUB文件
        try:
            self.book = epub.read_epub(self.epub_path)
            if self.book is None:
                raise ValueError(f"无法读取EPUB文件: {self.epub_path}")
        except Exception as e:
            if self.verbose:
                print(f"读取EPUB文件时出错: {e}")
            raise
        
        # 解析元数据
        self._parse_metadata()
        
        # 解析目录
        self._parse_toc()
        
        # 解析内容
        content = self._parse_content()
        
        # 解析图片
        self._parse_images()
        
        result = {
            'metadata': self.metadata,
            'toc': self.toc,
            'spine': self.spine,
            'content': content,
            'images': self.images
        }
        
        return result
    
    def _parse_metadata(self) -> None:
        """解析EPUB元数据"""
        if self.verbose:
            print("正在提取元数据...")
        
        if self.book is None:
            return
            
        # 提取标题
        title = self.book.get_metadata('DC', 'title')
        if title:
            self.metadata['title'] = title[0][0]
        
        # 提取作者
        creator = self.book.get_metadata('DC', 'creator')
        if creator:
            self.metadata['creator'] = creator[0][0]
        
        # 提取语言
        language = self.book.get_metadata('DC', 'language')
        if language:
            self.metadata['language'] = language[0][0]
        
        # 其他元数据
        identifiers = self.book.get_metadata('DC', 'identifier')
        if identifiers:
            self.metadata['identifier'] = identifiers[0][0]
        
        publishers = self.book.get_metadata('DC', 'publisher')
        if publishers:
            self.metadata['publisher'] = publishers[0][0]
        
        dates = self.book.get_metadata('DC', 'date')
        if dates:
            self.metadata['date'] = dates[0][0]
    
    def _parse_toc(self) -> None:
        """解析目录结构"""
        if self.verbose:
            print("正在提取目录结构...")
        
        if self.book is None:
            return
            
        def _process_toc_entries(entries, level=0):
            result = []
            for item in entries:
                if isinstance(item, tuple):
                    # 是目录项
                    title, href, children = item
                    entry = {
                        'title': title,
                        'href': href,
                        'level': level,
                        'children': _process_toc_entries(children, level + 1) if children else []
                    }
                    result.append(entry)
            return result
        
        self.toc = _process_toc_entries(self.book.toc)
        
        # 提取spine (内容顺序)
        self.spine = []
        for item in self.book.spine:
            # 处理不同类型的spine项
            if hasattr(item, 'get_id'):
                # EpubItem对象
                self.spine.append(item.get_id())
            elif isinstance(item, tuple) and len(item) >= 1:
                # 元组格式，第一个元素通常是ID
                self.spine.append(item[0])
            elif isinstance(item, str):
                # 字符串ID
                self.spine.append(item)
            else:
                # 尝试将对象转为字符串
                try:
                    item_id = str(item)
                    self.spine.append(item_id)
                except:
                    if self.verbose:
                        print(f"无法处理的spine项: {type(item)}")
                    continue
        
    def _parse_content(self) -> Dict[str, str]:
        """解析内容"""
        if self.verbose:
            print("正在提取内容...")
        
        content = {}
        
        if self.book is None:
            return content
            
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                item_id = item.get_id()
                html_content = item.get_content().decode('utf-8')
                content[item_id] = html_content
        
        return content
    
    def _parse_images(self) -> None:
        """提取图片资源"""
        if self.verbose:
            print("正在提取图片资源...")
        
        if self.book is None:
            return
            
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_IMAGE:
                item_id = item.get_id()
                image_data = item.get_content()
                file_name = os.path.basename(item.file_name)
                media_type = item.media_type
                
                self.images[item_id] = {
                    'data': image_data,
                    'file_name': file_name,
                    'media_type': media_type
                }
