"""
HTML到Markdown转换模块 - 负责将HTML内容转换为Markdown格式
"""

import re
import html2text
from bs4 import BeautifulSoup
import os

class HTMLToMarkdownConverter:
    """HTML到Markdown转换器"""
    
    def __init__(self, book_data, verbose=False):
        """
        初始化转换器
        
        Args:
            book_data (dict): 包含书籍内容的字典
            verbose (bool): 是否显示详细信息
        """
        self.book_data = book_data
        self.verbose = verbose
        self.markdown_content = {}
        
        # 配置html2text转换器
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_tables = False
        self.h2t.ignore_emphasis = False
        self.h2t.body_width = 0  # 不自动换行
        self.h2t.unicode_snob = True  # 使用Unicode字符
        self.h2t.single_line_break = True  # 不使用多行换行
    
    def convert(self):
        """
        将HTML内容转换为Markdown格式
        
        Returns:
            dict: 包含转换后的内容的字典
        """
        if self.verbose:
            print("正在将HTML转换为Markdown...")
        
        # 转换HTML内容
        for item_id, html_content in self.book_data['content'].items():
            if self.verbose:
                print(f"  处理章节: {item_id}")
            
            # 预处理HTML
            processed_html = self._preprocess_html(html_content)
            
            # 转换为Markdown
            markdown = self.h2t.handle(processed_html)
            
            # 后处理Markdown
            markdown = self._postprocess_markdown(markdown, item_id)
            
            self.markdown_content[item_id] = markdown
        
        # 更新图片引用路径
        self._update_image_paths()
        
        result = {
            'metadata': self.book_data['metadata'],
            'toc': self.book_data['toc'],
            'spine': self.book_data['spine'],
            'content': self.markdown_content,
            'images': self.book_data['images']
        }
        
        return result
    
    def _preprocess_html(self, html_content):
        """
        预处理HTML内容
        
        Args:
            html_content (str): HTML内容
            
        Returns:
            str: 处理后的HTML
        """
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 处理标题
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                # 确保标题前后有空行
                if heading.string:
                    heading_text = heading.string
                    new_tag = soup.new_tag(f'h{i}')
                    new_tag.string = heading_text
                    heading.replace_with(new_tag)
        
        # 处理图片
        for img in soup.find_all('img'):
            # 确保图片有alt属性
            if not img.get('alt'):
                img['alt'] = os.path.basename(img.get('src', ''))
        
        return str(soup)
    
    def _postprocess_markdown(self, markdown, item_id):
        """
        后处理Markdown内容
        
        Args:
            markdown (str): Markdown内容
            item_id (str): 内容ID
            
        Returns:
            str: 处理后的Markdown
        """
        # 修复标题格式
        markdown = re.sub(r'^(#+)(.*?)$', r'\1 \2', markdown, flags=re.MULTILINE)
        
        # 修复列表格式问题
        markdown = re.sub(r'^(\s*[-*+])\s{2,}', r'\1 ', markdown, flags=re.MULTILINE)
        
        # 确保段落之间有空行
        markdown = re.sub(r'([^\n])\n([^\n])', r'\1\n\n\2', markdown)
        
        # 删除多余的空行
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        return markdown
    
    def _update_image_paths(self):
        """更新Markdown中的图片引用路径"""
        # 创建图片ID到文件名的映射
        image_mapping = {}
        for img_id, img_data in self.book_data['images'].items():
            file_name = img_data['file_name']
            image_mapping[img_id] = file_name
        
        # 更新每个章节中的图片引用
        for item_id, markdown in self.markdown_content.items():
            for img_id, file_name in image_mapping.items():
                # 寻找可能的引用格式
                possible_refs = [
                    f"({img_id})",
                    f"({os.path.basename(img_id)})"
                ]
                
                for ref in possible_refs:
                    # 替换为相对路径
                    if ref in markdown:
                        markdown = markdown.replace(ref, f"(images/{file_name})")
            
            self.markdown_content[item_id] = markdown
