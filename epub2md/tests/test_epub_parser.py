"""
EPUB解析器测试
"""
import os
import unittest
from unittest.mock import patch, Mock
from epub2md.epub_parser import EPUBParser
import ebooklib
from ebooklib import epub


class TestEPUBParser(unittest.TestCase):
    """测试EPUB解析器"""
    
    def setUp(self):
        """测试前准备"""
        # 创建模拟的EPUB内容
        self.mock_book = Mock()
        self.mock_book.get_metadata.side_effect = self._mock_get_metadata
        self.mock_book.toc = [
            ('Chapter 1', 'chapter1.xhtml', []),
            ('Chapter 2', 'chapter2.xhtml', [
                ('Section 2.1', 'chapter2.xhtml#section1', [])
            ])
        ]
        self.mock_book.spine = [Mock(get_id=lambda: 'item1'), Mock(get_id=lambda: 'item2')]
        
        self.mock_items = [
            Mock(get_type=lambda: ebooklib.ITEM_DOCUMENT, get_id=lambda: 'item1', 
                get_content=lambda: b'<html><body><h1>Chapter 1</h1><p>Content</p></body></html>'),
            Mock(get_type=lambda: ebooklib.ITEM_DOCUMENT, get_id=lambda: 'item2', 
                get_content=lambda: b'<html><body><h1>Chapter 2</h1><p>Content</p></body></html>'),
            Mock(get_type=lambda: ebooklib.ITEM_IMAGE, get_id=lambda: 'image1', 
                get_content=lambda: b'image_data', file_name='image.jpg', media_type='image/jpeg')
        ]
        self.mock_book.get_items.return_value = self.mock_items
    
    def _mock_get_metadata(self, namespace, name):
        """模拟获取元数据"""
        metadata = {
            'title': [('Test Book', {})],
            'creator': [('Test Author', {})],
            'language': [('zh-CN', {})],
            'identifier': [('12345', {})],
            'publisher': [('Test Publisher', {})],
            'date': [('2023-01-01', {})]
        }
        return metadata.get(name, [])
    
    @patch('epub2md.epub_parser.epub.read_epub')
    def test_parse(self, mock_read_epub):
        """测试解析方法"""
        # 设置模拟
        mock_read_epub.return_value = self.mock_book
        
        # 创建解析器
        parser = EPUBParser('test.epub')
        result = parser.parse()
        
        # 验证元数据
        self.assertEqual(result['metadata']['title'], 'Test Book')
        self.assertEqual(result['metadata']['creator'], 'Test Author')
        self.assertEqual(result['metadata']['language'], 'zh-CN')
        
        # 验证目录
        self.assertEqual(len(result['toc']), 2)
        self.assertEqual(result['toc'][0]['title'], 'Chapter 1')
        self.assertEqual(result['toc'][1]['title'], 'Chapter 2')
        self.assertEqual(len(result['toc'][1]['children']), 1)
        
        # 验证spine
        self.assertEqual(result['spine'], ['item1', 'item2'])
        
        # 验证内容
        self.assertIn('item1', result['content'])
        self.assertIn('item2', result['content'])
        
        # 验证图片
        self.assertIn('image1', result['images'])
        self.assertEqual(result['images']['image1']['file_name'], 'image.jpg')
        self.assertEqual(result['images']['image1']['media_type'], 'image/jpeg')


if __name__ == '__main__':
    unittest.main() 