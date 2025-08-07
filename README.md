Smart Image Compressor 智能图片批量压缩工具

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一款功能强大的 Python 图片批量压缩工具，智能、高效、易用。

An intelligent and powerful batch image compression tool powered by Python.



功能亮点 (Features)

*   ** 智能质量探测**: 自动在设定的质量范围内寻找最佳压缩比，平衡文件大小和视觉质量。
*   ** 透明通道自动识别**: 自动检测图片是否包含透明通道，并选择最佳格式（PNG 用于透明图，JPEG 用于不透明图）进行压缩。
*   ** 递归目录处理**: 支持递归处理整个文件夹及其所有子文件夹中的图片。
*   ** 详细压缩报告**: 任务完成后，生成详细的统计报告，包括处理数量、节省空间、平均压缩率和总耗时。
*   ** 多格式支持**: 支持压缩最常见的网络图片格式：`JPEG` 和 `PNG`。
*   ** 高度可定制**: 可通过参数轻松调整压缩质量、覆盖选项等。

安装 (Installation)

1.  克隆本仓库到本地：
    git clone https://github.com/RealYasuHaru/Smart-Image-Compressor.git

    cd Smart-Image-Compressor

3.  安装依赖项 (Pillow):

    pip install -r requirements.txt
  
使用方法 (Usage)

方式一：直接修改脚本 (v2.1)

这是最直接的运行方式。

1.  将您需要压缩的图片或图片文件夹放入 `input_images` 目录（如果不存在，请手动创建）。
2.  打开 `compressor.py` 文件 。
3.  在文件底部的 `if __name__ == "__main__":` 部分，根据您的需求修改参数：

    if __name__ == "__main__":
    
        # 直接在代码中设置参数
    
        input_path = "input_images/"  # 输入路径（文件或目录）
    
        output_dir = "output_images/"    # 输出目录路径
    
        quality = 85              # 初始质量参数 (默认: 85)
    
        max_reduction = 25        # 最大质量降幅 (默认: 25)
    
        overwrite = False         # 是否覆盖已存在文件 (默认: False)
    
        recurse = True            # 是否递归处理子目录 (默认: True)
    
    


4.  运行脚本：

    python3 compressor.py

5.  压缩后的图片将保留原始目录结构，并保存在 `output_images` 文件夹中。

方式二：使用命令行参数 (推荐)

压缩单个文件
python3 compressor.py "input_images/logo.png" -o "output_images/"

压缩整个目录（非递归）
python3 compressor.py "input_images/" -o "output_images/"

递归压缩整个目录，并设置初始质量为90
python3 compressor.py "input_images/" -o "output_images/" -r -q 90

查看帮助
python3 compressor.py -h


#效果演示 (Example Output)


脚本运行后，您会看到类似下面的输出：

发现 5 个待处理文件

处理中 (1/5): input_images/scenery.jpg

压缩完成: input_images/scenery.jpg

尺寸: 850.2KB → 150.5KB

压缩率: 17.7% | 最终质量: 80


处理中 (2/5): input_images/transparent_logo.png

跳过已存在文件: output_images/transparent_logo.png

处理中 (3/5): input_images/subdir/icon.png

压缩完成: input_images/subdir/icon.png

尺寸: 55.1KB → 12.3KB

压缩率: 22.3% | 最终质量: 85


==================================================

压缩报告

==================================================

总文件数:   5

成功处理:   4

跳过文件:   1

失败文件:   0


原始大小:  1.25 MB

压缩大小:  0.28 MB

平均压缩率: 22.4%

节省空间:  0.97 MB


总耗时:    2.1秒
==================================================

### 📄 许可证 (License)

本项目采用 [MIT License](LICENSE) 授权。
