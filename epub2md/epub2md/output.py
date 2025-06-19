"""
输出处理模块 - 负责生成Markdown输出文件
"""

import os
import shutil
import re
from .resource import ResourceProcessor

class OutputGenerator:
    """Markdown输出生成器"""
    
    def __init__(self, book_data, output_path, single_file=False, include_toc=True, verbose=False):
        """
        初始化输出生成器
        
        Args:
            book_data (dict): 包含书籍内容的字典
            output_path (str): 输出路径
            single_file (bool): 是否输出为单个文件
            include_toc (bool): 是否包含目录
            verbose (bool): 是否显示详细信息
        """
        self.book_data = book_data
        self.output_path = output_path
        self.single_file = single_file
        self.include_toc = include_toc
        self.verbose = verbose
        
        # 确定输出目录
        if self.single_file:
            self.output_dir = os.path.dirname(output_path) or '.'
        else:
            self.output_dir = output_path
            
        # 资源处理器
        self.resource_processor = None
        
        # 章节信息映射
        self.chapter_files = {}  # 章节ID到文件名的映射
        self.chapter_titles = {}  # 章节ID到标题的映射
        self.chapter_sequence = []  # 按顺序排列的章节ID
    
    def generate(self):
        """生成Markdown输出"""
        if self.verbose:
            print(f"正在生成Markdown输出...")
            print(f"输出模式: {'单文件' if self.single_file else '多文件'}")
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 处理资源
        self.resource_processor = ResourceProcessor(self.book_data, self.output_dir, self.verbose)
        self.resource_processor.process_resources()
        
        # 准备章节映射和序列
        self._prepare_chapter_info()
        
        if self.single_file:
            self._generate_single_file()
        else:
            self._generate_multiple_files()
    
    def _prepare_chapter_info(self):
        """准备章节信息，包括文件名、标题和顺序"""
        # 遍历spine获取章节顺序
        for idx, item_id in enumerate(self.book_data['spine']):
            if item_id in self.book_data['content']:
                self.chapter_sequence.append(item_id)
                
                # 获取章节标题
                chapter_title = self._get_chapter_title(item_id) or f"第{idx+1}章"
                self.chapter_titles[item_id] = chapter_title
                
                # 生成文件名
                chapter_number = f"{idx+1:02d}-"
                safe_title = self._make_safe_filename(chapter_title)
                file_name = f"{chapter_number}{safe_title}.md"
                self.chapter_files[item_id] = file_name
    
    def _generate_single_file(self):
        """生成单个Markdown文件"""
        if self.verbose:
            print("正在生成单个Markdown文件...")
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            # 写入元数据
            self._write_metadata(f)
            f.write('\n\n')
            
            # 写入目录
            if self.include_toc:
                self._write_toc(f)
                f.write('\n\n')
            
            # 写入内容
            self._write_content(f)
    
    def _generate_multiple_files(self):
        """生成多个Markdown文件"""
        if self.verbose:
            print("正在生成多个Markdown文件...")
        
        # 生成主文件
        main_file_path = os.path.join(self.output_dir, 'README.md')
        with open(main_file_path, 'w', encoding='utf-8') as f:
            # 写入元数据
            self._write_metadata(f)
            f.write('\n\n')
            
            # 写入目录
            if self.include_toc:
                self._write_toc(f, is_main_file=True)
        
        # 为每个章节生成单独的文件
        for idx, item_id in enumerate(self.chapter_sequence):
            if self.verbose:
                print(f"  正在生成章节: {item_id}")
            
            # 获取章节标题和文件名
            chapter_title = self.chapter_titles.get(item_id, f"第{idx+1}章")
            file_name = self.chapter_files.get(item_id, f"{idx+1:02d}.md")
            file_path = os.path.join(self.output_dir, file_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                # 1. 添加导航链接 (顶部)
                self._write_nav_links(f, item_id, position='top')
                
                # 2. 写入章节标题
                f.write(f"# {chapter_title}\n\n")
                
                # 3. 写入章节内容
                content = self.book_data['content'].get(item_id, '')
                f.write(content)
                f.write('\n\n')
                
                # 4. 添加导航链接 (底部)
                self._write_nav_links(f, item_id, position='bottom')
    
    def _write_metadata(self, file):
        """
        写入元数据
        
        Args:
            file: 文件对象
        """
        metadata = self.book_data['metadata']
        
        # 写入标题
        if 'title' in metadata:
            file.write(f"# {metadata['title']}\n\n")
        
        # 写入作者
        if 'creator' in metadata:
            file.write(f"作者: {metadata['creator']}\n\n")
        
        # 其他元数据
        if 'publisher' in metadata:
            file.write(f"出版社: {metadata['publisher']}\n")
        
        if 'date' in metadata:
            file.write(f"日期: {metadata['date']}\n")
        
        if 'language' in metadata:
            file.write(f"语言: {metadata['language']}\n")
    
    def _write_toc(self, file, is_main_file=False):
        """
        写入目录
        
        Args:
            file: 文件对象
            is_main_file: 是否为主文件
        """
        file.write("## 目录\n\n")
        
        def write_toc_entries(entries, level=0):
            for entry in entries:
                indent = '  ' * level
                title = entry['title']
                href = entry['href']
                
                # 在多文件模式下，链接到对应的文件
                if is_main_file and not self.single_file:
                    # 找到对应的章节ID
                    chapter_id = self._get_chapter_id_from_href(href)
                    if chapter_id:
                        # 使用预先生成的文件名
                        if chapter_id in self.chapter_files:
                            href = self.chapter_files[chapter_id]
                        else:
                            # 如果没有预生成的文件名，使用章节标题生成
                            chapter_title = self._get_chapter_title(chapter_id)
                            if chapter_title:
                                safe_title = self._make_safe_filename(chapter_title)
                                href = f"{safe_title}.md"
                            else:
                                href = f"{chapter_id}.md"
                
                # 在单文件模式下，创建内部锚链接
                elif self.single_file and chapter_id:
                    # 创建锚点
                    anchor = self._make_anchor_id(self.chapter_titles.get(chapter_id, title))
                    href = f"#{anchor}"
                        
                file.write(f"{indent}- [{title}]({href})\n")
                
                # 递归处理子目录
                if entry['children']:
                    write_toc_entries(entry['children'], level + 1)
        
        write_toc_entries(self.book_data['toc'])
    
    def _write_content(self, file):
        """
        写入内容
        
        Args:
            file: 文件对象
        """
        # 按spine顺序写入内容
        for item_id in self.chapter_sequence:
            if item_id in self.book_data['content']:
                # 获取章节标题
                chapter_title = self.chapter_titles.get(item_id)
                
                if chapter_title:
                    # 创建锚点
                    anchor_id = self._make_anchor_id(chapter_title)
                    file.write(f'<a id="{anchor_id}"></a>\n\n')
                    file.write(f"# {chapter_title}\n\n")
                
                content = self.book_data['content'][item_id]
                file.write(content)
                file.write('\n\n')
    
    def _write_nav_links(self, file, current_chapter_id, position='top'):
        """
        写入章节间导航链接
        
        Args:
            file: 文件对象
            current_chapter_id: 当前章节ID
            position: 位置 ('top' 或 'bottom')
        """
        try:
            current_idx = self.chapter_sequence.index(current_chapter_id)
        except ValueError:
            return
        
        # 获取上一章和下一章
        prev_chapter_id = self.chapter_sequence[current_idx - 1] if current_idx > 0 else None
        next_chapter_id = self.chapter_sequence[current_idx + 1] if current_idx < len(self.chapter_sequence) - 1 else None
        
        if position == 'top':
            file.write('[ [目录](README.md) ]')
            
            if prev_chapter_id:
                prev_title = self.chapter_titles.get(prev_chapter_id, "上一章")
                prev_file = self.chapter_files.get(prev_chapter_id, "")
                file.write(f' [ [← {prev_title}]({prev_file}) ]')
                
            if next_chapter_id:
                next_title = self.chapter_titles.get(next_chapter_id, "下一章")
                next_file = self.chapter_files.get(next_chapter_id, "")
                file.write(f' [ [{next_title} →]({next_file}) ]')
                
            file.write('\n\n---\n\n')
            
        elif position == 'bottom':
            file.write('\n\n---\n\n')
            file.write('[ [目录](README.md) ]')
            
            if prev_chapter_id:
                prev_title = self.chapter_titles.get(prev_chapter_id, "上一章")
                prev_file = self.chapter_files.get(prev_chapter_id, "")
                file.write(f' [ [← {prev_title}]({prev_file}) ]')
                
            if next_chapter_id:
                next_title = self.chapter_titles.get(next_chapter_id, "下一章")
                next_file = self.chapter_files.get(next_chapter_id, "")
                file.write(f' [ [{next_title} →]({next_file}) ]')
                
            file.write('\n')
    
    def _get_chapter_title(self, item_id):
        """
        根据章节ID获取标题
        
        Args:
            item_id: 章节ID
            
        Returns:
            str: 章节标题，如果没有找到则返回None
        """
        # 在目录中查找
        def find_title_in_toc(entries):
            for entry in entries:
                href = entry['href']
                chapter_id = self._get_chapter_id_from_href(href)
                
                if chapter_id == item_id:
                    return entry['title']
                
                # 递归查找子目录
                if entry['children']:
                    title = find_title_in_toc(entry['children'])
                    if title:
                        return title
            
            return None
        
        return find_title_in_toc(self.book_data['toc'])
    
    def _get_chapter_id_from_href(self, href):
        """
        从href中提取章节ID
        
        Args:
            href: href属性值
            
        Returns:
            str: 章节ID，如果无法提取则返回None
        """
        # 提取文件名
        if '#' in href:
            href = href.split('#')[0]
        
        # 提取文件名（不带路径）
        file_name = os.path.basename(href)
        
        # 查找匹配的内容项
        for item_id, content in self.book_data['content'].items():
            # 通常EPUB会在文件名部分使用内容ID
            if item_id in file_name or file_name in item_id:
                return item_id
        
        return None
    
    def _make_safe_filename(self, title):
        """
        生成安全的文件名
        
        Args:
            title: 标题
            
        Returns:
            str: 安全的文件名
        """
        # 使用拼音化处理中文字符 (可选)
        
        # 删除不安全的字符
        unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']
        safe_title = title
        
        for char in unsafe_chars:
            safe_title = safe_title.replace(char, '_')
        
        # 替换多个连续下划线为单个
        safe_title = re.sub(r'_+', '_', safe_title)
        
        # 去除开头和结尾的下划线
        safe_title = safe_title.strip('_')
        
        # 限制长度
        if len(safe_title) > 50:
            safe_title = safe_title[:50]
        
        return safe_title
    
    def _make_anchor_id(self, text):
        """
        根据文本生成HTML锚点ID
        
        Args:
            text: 文本
            
        Returns:
            str: 安全的锚点ID
        """
        # 转为小写
        anchor = text.lower()
        
        # 删除不允许的字符
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        
        # 将空格替换为短横线
        anchor = re.sub(r'\s+', '-', anchor)
        
        # 替换多个连续短横线为单个
        anchor = re.sub(r'-+', '-', anchor)
        
        # 去除开头和结尾的短横线
        anchor = anchor.strip('-')
        
        return anchor
