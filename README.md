# 文件复制移动工具

一个简单易用的文件复制和移动工具，使用Python和Tkinter构建的GUI应用程序。

## 功能特点
- 直观的图形用户界面
- 支持文件和文件夹的复制操作
- 支持文件和文件夹的移动操作
- 操作进度显示
- 错误处理和提示

## 安装方法

### 直接使用可执行文件
1. 从dist文件夹中下载`文件复制移动工具.exe`
2. 双击运行即可，无需安装Python环境

### 从源代码运行
1. 克隆本仓库
```
git clone https://github.com/yourusername/file-copy-move-tool.git
cd file-copy-move-tool
```

2. 安装依赖
```
pip install -r requirements.txt
```

3. 运行应用程序
```
python 从X复制到Y-3.py
```

## 使用方法
1. 选择源文件/文件夹路径
2. 选择目标路径
3. 点击复制或移动按钮
4. 查看操作进度和结果

## 项目结构
- `从X复制到Y-3.py`: 主应用程序文件
- `icon.py` 和 `icon_rc.py`: 图标资源文件
- `dabao.spec`: PyInstaller打包配置文件
- `dist/`: 包含打包后的可执行文件
- `build/`: 打包过程中的临时文件

## 打包应用
如果需要重新打包应用程序，可以使用以下命令：
```
pyinstaller dabao.spec
```

## 许可证
[MIT](LICENSE)
