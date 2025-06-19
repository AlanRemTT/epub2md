"""
资源处理模块 - 负责处理图片等资源文件
"""

import os
import shutil
from PIL import Image
from io import BytesIO

class ResourceProcessor:
    """资源处理器，处理EPUB中的资源文件（主要是图片）"""
    
    def __init__(self, book_data, output_dir, verbose=False):
        """
        初始化资源处理器
        
        Args:
            book_data (dict): 包含书籍内容的字典
            output_dir (str): 输出目录
            verbose (bool): 是否显示详细信息
        """
        self.book_data = book_data
        self.output_dir = output_dir
        self.verbose = verbose
        self.image_dir = os.path.join(output_dir, 'images')
        self.processed_images = {}
    
    def process_resources(self):
        """
        处理所有资源文件
        
        Returns:
            dict: 处理后的资源映射
        """
        if self.verbose:
            print("正在处理资源文件...")
        
        # 确保图片目录存在
        os.makedirs(self.image_dir, exist_ok=True)
        
        # 处理图片
        self._process_images()
        
        return self.processed_images
    
    def _process_images(self):
        """处理图片文件"""
        if self.verbose:
            print("正在处理图片资源...")
        
        for img_id, img_data in self.book_data['images'].items():
            try:
                image_data = img_data['data']
                file_name = img_data['file_name']
                media_type = img_data['media_type']
                
                # 构建输出路径
                output_path = os.path.join(self.image_dir, file_name)
                
                # 检查文件是否已存在
                if os.path.exists(output_path):
                    # 生成唯一文件名
                    base_name, ext = os.path.splitext(file_name)
                    file_name = f"{base_name}_{img_id}{ext}"
                    output_path = os.path.join(self.image_dir, file_name)
                
                # 根据媒体类型处理
                if 'image/svg' in media_type:
                    # 直接写入SVG文件
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                else:
                    try:
                        # 使用PIL处理图片
                        img = Image.open(BytesIO(image_data))
                        
                        # 优化输出
                        if media_type == 'image/jpeg' or media_type == 'image/jpg':
                            img.save(output_path, 'JPEG', quality=90, optimize=True)
                        elif media_type == 'image/png':
                            img.save(output_path, 'PNG', optimize=True)
                        elif media_type == 'image/gif':
                            img.save(output_path, 'GIF')
                        else:
                            # 其他类型直接写入
                            with open(output_path, 'wb') as f:
                                f.write(image_data)
                    except Exception as e:
                        # 如果出错，直接写入原始数据
                        if self.verbose:
                            print(f"  处理图片时出错: {e}，直接写入原始数据")
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                
                # 记录处理结果
                self.processed_images[img_id] = {
                    'original_file': img_data['file_name'],
                    'processed_file': file_name,
                    'output_path': output_path,
                    'media_type': media_type
                }
                
                if self.verbose:
                    print(f"  已处理图片: {file_name}")
                    
            except Exception as e:
                if self.verbose:
                    print(f"  处理图片 {img_id} 时出错: {e}")
    
    def cleanup(self):
        """清理临时资源"""
        # 检查是否有需要清理的临时文件
        pass
