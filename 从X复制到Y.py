import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import shutil
from pathlib import Path
import threading
import base64
from io import BytesIO
from PIL import Image, ImageTk
from icon_rc import icon_data

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件/文件夹复制移动工具")
        self.root.geometry("600x650+500+200")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 设置统一的按钮宽度
        button_width = 24
        
        # 源路径选择
        ttk.Label(main_frame, text="源路径:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.source_path = tk.StringVar()
        source_entry = ttk.Entry(main_frame, textvariable=self.source_path, width=40)
        source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5))
        ttk.Button(main_frame, text="浏览", command=self.browse_source, width=button_width).grid(row=0, column=2, padx=(5, 0), sticky=tk.EW)
        
        # 目标路径选择
        ttk.Label(main_frame, text="目标路径:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.dest_path = tk.StringVar()
        dest_entry = ttk.Entry(main_frame, textvariable=self.dest_path, width=40)
        dest_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5))
        ttk.Button(main_frame, text="浏览", command=self.browse_dest, width=button_width).grid(row=1, column=2, padx=(5, 0), sticky=tk.EW)
        
        # 创建选项区域框架
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # 操作类型选择
        ttk.Label(options_frame, text="操作类型:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.operation_type = tk.StringVar(value="copy")
        op_frame = ttk.Frame(options_frame)
        op_frame.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        ttk.Radiobutton(op_frame, text="复制", variable=self.operation_type, value="copy").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(op_frame, text="移动", variable=self.operation_type, value="move").pack(side=tk.LEFT)
        
        # 对象类型选择
        ttk.Label(options_frame, text="对象类型:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.object_type = tk.StringVar(value="file")
        obj_frame = ttk.Frame(options_frame)
        obj_frame.grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(obj_frame, text="全部", variable=self.object_type, value="all").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(obj_frame, text="仅文件", variable=self.object_type, value="file").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(obj_frame, text="仅文件夹", variable=self.object_type, value="folder").pack(side=tk.LEFT)
        
        # 匹配模式选择
        ttk.Label(options_frame, text="匹配模式:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.match_mode = tk.StringVar(value="prefix")
        match_frame = ttk.Frame(options_frame)
        match_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        ttk.Radiobutton(match_frame, text="精确匹配", variable=self.match_mode, value="exact").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(match_frame, text="前缀匹配", variable=self.match_mode, value="prefix").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(match_frame, text="后缀匹配", variable=self.match_mode, value="suffix").pack(side=tk.LEFT)
        
        # 冲突处理规则
        ttk.Label(options_frame, text="冲突处理:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.conflict_mode = tk.StringVar(value="skip")
        conflict_frame = ttk.Frame(options_frame)
        conflict_frame.grid(row=3, column=1, columnspan=3, sticky=tk.W)
        ttk.Radiobutton(conflict_frame, text="跳过", variable=self.conflict_mode, value="skip").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(conflict_frame, text="替换", variable=self.conflict_mode, value="replace").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(conflict_frame, text="合并", variable=self.conflict_mode, value="merge").pack(side=tk.LEFT)
        
        # 按钮区域 - 与浏览按钮对齐
        ttk.Button(main_frame, text="开始执行", command=self.start_operation, width=button_width).grid(row=2, column=2, padx=(5, 0), sticky=tk.EW, pady=(15, 0))
        ttk.Button(main_frame, text="清空日志", command=self.clear_log, width=button_width).grid(row=2, column=2, padx=(5, 0), sticky=tk.EW, pady=(15, 60))
        
        # 内容区域框架
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(1, weight=1)
        
        # 文件/文件夹名称列表
        ttk.Label(content_frame, text="名称列表 (每行一个):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.names_text = scrolledtext.ScrolledText(content_frame, width=40, height=15, wrap=tk.WORD)
        self.names_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 操作日志
        ttk.Label(content_frame, text="操作日志:").grid(row=0, column=1, sticky=tk.W)
        self.log_text = scrolledtext.ScrolledText(content_frame, width=40, height=15, wrap=tk.WORD)
        self.log_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 尝试使用Base64数据加载图标
        try:
            # 移除可能的前缀并解码Base64数据
            # 处理数据
            clean_data = icon_data.split(',')[-1].strip()  # 移除可能的data URI前缀和空白字符
            
            # 填充Base64数据（如果长度不是4的倍数）
            padding = len(clean_data) % 4
            if padding > 0:
                clean_data += '=' * (4 - padding)
            
            try:
                icon_bytes = base64.b64decode(clean_data, validate=True)
                #self.log_message(f"Base64解码成功，获得{len(icon_bytes)}字节图像数据")
                icon_io = BytesIO(icon_bytes)
                
                # 尝试识别图像格式
                pil_image = Image.open(icon_io)
                #self.log_message(f"图像格式识别成功: {pil_image.format}, 尺寸: {pil_image.size}")
                
                # 转换为Tkinter可用格式
                self.icon = ImageTk.PhotoImage(pil_image)
                self.root.iconphoto(True, self.icon)
                #self.log_message("成功从Base64数据加载图标")
            except base64.binascii.Error as e:
                self.log_message(f"Base64严格解码失败: {str(e)}")
                # 尝试非严格模式解码
                try:
                    icon_bytes = base64.b64decode(clean_data, validate=False)
                    self.log_message(f"Base64非严格模式解码成功，获得{len(icon_bytes)}字节数据")
                    icon_io = BytesIO(icon_bytes)
                    pil_image = Image.open(icon_io)
                    self.icon = ImageTk.PhotoImage(pil_image)
                    self.root.iconphoto(True, self.icon)
                    self.log_message("成功使用非严格模式加载图标")
                except Exception as e2:
                    self.log_message(f"非严格模式解码失败: {str(e2)}")
        except base64.binascii.Error as e:
            self.log_message(f"Base64解码错误: {str(e)}")
            if len(clean_data) % 4 != 0:
                self.log_message(f"Base64数据长度异常: {len(clean_data)}字节，不是4的倍数")
        except Exception as e:
            self.log_message(f"图标加载失败: {str(e)}")
        
        # 配置主框架行权重
        main_frame.rowconfigure(4, weight=1)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def browse_source(self):
        """浏览源路径"""
        path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)
    
    def browse_dest(self):
        """浏览目标路径"""
        path = filedialog.askdirectory()
        if path:
            self.dest_path.set(path)
    
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.progress['value'] = 0
    
    def get_matching_items(self, source_dir, names, match_mode):
        """获取匹配的文件和文件夹"""
        matching_items = []
        
        if not os.path.exists(source_dir):
            self.log_message(f"错误: 源路径不存在 - {source_dir}")
            return matching_items
        
        for name in names:
            name = name.strip()
            if not name:
                continue
                
            found = False
            
            # 遍历源目录中的所有项目
            for item in os.listdir(source_dir):
                item_path = os.path.join(source_dir, item)
                
                # 检查匹配模式
                if match_mode == "exact":
                    match = item == name
                elif match_mode == "prefix":
                    match = item.startswith(name)
                else:  # suffix
                    match = item.endswith(name)
                
                if match:
                    is_file = os.path.isfile(item_path)
                    is_dir = os.path.isdir(item_path)
                    
                    # 根据对象类型筛选
                    obj_type = self.object_type.get()
                    if obj_type == 'file' and not is_file:
                        continue
                    if obj_type == 'folder' and not is_dir:
                        continue
                    
                    if is_file or is_dir:
                        matching_items.append({
                            'name': item,
                            'path': item_path,
                            'type': 'file' if is_file else 'folder'
                        })
                        found = True
                        self.log_message(f"找到{'文件' if is_file else '文件夹'}: {item}")
            
            if not found:
                self.log_message(f"未找到匹配项: {name}")
        
        return matching_items
    
    def copy_item(self, src_path, dest_path, item_type, conflict_mode):
        """复制文件或文件夹"""
        try:
            if os.path.exists(dest_path):
                if conflict_mode == "skip":
                    self.log_message(f"跳过已存在的项目: {dest_path}")
                    return True
                elif conflict_mode == "replace":
                    if item_type == "file":
                        os.remove(dest_path)
                    else:  # folder
                        shutil.rmtree(dest_path)
                    self.log_message(f"已删除现有项目: {dest_path}")
                # merge模式不需要删除，直接覆盖或合并
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            if item_type == "file":
                shutil.copy2(src_path, dest_path)
            else:  # folder
                if conflict_mode == "merge" and os.path.exists(dest_path):
                    # 合并文件夹
                    self.merge_folders(src_path, dest_path)
                else:
                    shutil.copytree(src_path, dest_path)
            
            self.log_message(f"复制成功: {src_path} -> {dest_path}")
            return True
            
        except Exception as e:
            self.log_message(f"复制失败: {src_path} -> {dest_path}, 错误: {str(e)}")
            return False
    
    def merge_folders(self, src_folder, dest_folder):
        """合并文件夹"""
        for item in os.listdir(src_folder):
            src_item = os.path.join(src_folder, item)
            dest_item = os.path.join(dest_folder, item)
            
            if os.path.isfile(src_item):
                shutil.copy2(src_item, dest_item)
            elif os.path.isdir(src_item):
                if os.path.exists(dest_item):
                    self.merge_folders(src_item, dest_item)
                else:
                    shutil.copytree(src_item, dest_item)
    
    def move_item(self, src_path, dest_path, item_type, conflict_mode):
        """移动文件或文件夹"""
        try:
            if os.path.exists(dest_path):
                if conflict_mode == "skip":
                    self.log_message(f"跳过已存在的项目: {dest_path}")
                    return True
                elif conflict_mode == "replace":
                    if item_type == "file":
                        os.remove(dest_path)
                    else:  # folder
                        shutil.rmtree(dest_path)
                    self.log_message(f"已删除现有项目: {dest_path}")
                elif conflict_mode == "merge" and item_type == "folder":
                    # 先合并，再删除源文件夹
                    self.merge_folders(src_path, dest_path)
                    shutil.rmtree(src_path)
                    self.log_message(f"合并移动成功: {src_path} -> {dest_path}")
                    return True
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            shutil.move(src_path, dest_path)
            self.log_message(f"移动成功: {src_path} -> {dest_path}")
            return True
            
        except Exception as e:
            self.log_message(f"移动失败: {src_path} -> {dest_path}, 错误: {str(e)}")
            return False
    
    def perform_operation(self):
        """执行文件操作"""
        source_dir = self.source_path.get().strip()
        dest_dir = self.dest_path.get().strip()
        operation = self.operation_type.get()
        match_mode = self.match_mode.get()
        conflict_mode = self.conflict_mode.get()
        
        # 验证输入
        if not source_dir or not dest_dir:
            messagebox.showerror("错误", "请选择源路径和目标路径")
            return
        
        if not os.path.exists(source_dir):
            messagebox.showerror("错误", "源路径不存在")
            return
        
        names_content = self.names_text.get(1.0, tk.END).strip()
        if not names_content:
            messagebox.showerror("错误", "请输入要处理的文件或文件夹名称")
            return
        
        names = [name.strip() for name in names_content.split('\n') if name.strip()]
        
        self.log_message(f"开始执行{'复制' if operation == 'copy' else '移动'}操作...")
        self.log_message(f"源路径: {source_dir}")
        self.log_message(f"目标路径: {dest_dir}")
        self.log_message(f"匹配模式: {'精确匹配' if match_mode == 'exact' else '前缀匹配'}")
        self.log_message(f"冲突处理: {conflict_mode}")
        self.log_message(f"处理项目数量: {len(names)}")
        self.log_message("-" * 50)
        
        # 获取匹配的项目
        matching_items = self.get_matching_items(source_dir, names, match_mode)
        
        if not matching_items:
            self.log_message("没有找到匹配的项目")
            return
        
        # 执行操作
        success_count = 0
        self.progress['maximum'] = len(matching_items)
        
        for item in matching_items:
            src_path = item['path']
            dest_path = os.path.join(dest_dir, item['name'])
            
            if operation == "copy":
                if self.copy_item(src_path, dest_path, item['type'], conflict_mode):
                    success_count += 1
                    self.progress['value'] = success_count
            else:  # move
                if self.move_item(src_path, dest_path, item['type'], conflict_mode):
                    success_count += 1
                    self.progress['value'] = success_count
        
        self.log_message("-" * 50)
        self.log_message(f"操作完成! 成功处理 {success_count}/{len(matching_items)} 个项目")
    
    def start_operation(self):
        """开始操作（在新线程中执行）"""
        self.progress['value'] = 0
        
        def run_operation():
            try:
                self.perform_operation()
            finally:
                pass
        
        thread = threading.Thread(target=run_operation, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
    # ... existing code ...