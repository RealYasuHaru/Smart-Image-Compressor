#!/usr/bin/env python3

import os
import time
import argparse
from pathlib import Path
from PIL import Image

class SmartImageCompressor:
    def __init__(self):
        self.stats = {
            'total': 0,
            'processed': 0,
            'skipped': 0,
            'failed': 0,
            'original_size': 0,
            'compressed_size': 0,
            'start_time': 0
        }

    def optimize_image(self, input_path: Path, output_path: Path, quality: int, max_reduction: int, overwrite: bool) -> bool:
        if not overwrite and output_path.exists():
            self.stats['skipped'] += 1
            print(f"跳过已存在文件: {output_path}")
            return False

        try:
            with Image.open(input_path) as img:
                original_size = input_path.stat().st_size
                best_quality = quality
                best_size = float('inf')

                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img_format = 'PNG'
                    img = img.convert('RGBA')
                else:
                    img_format = 'JPEG'
                    img = img.convert('RGB')

                for q in range(quality, quality - max_reduction - 1, -5):
                    if q <= 0: continue
                    try:
                        save_args = {
                            'format': img_format,
                            'quality': q,
                            'optimize': True,
                        }
                        if img_format == 'JPEG':
                            save_args['progressive'] = True
                        elif img_format == 'PNG':
                            save_args['compress_level'] = 9 

                        img.save(output_path, **save_args)
                        current_size = output_path.stat().st_size

                        if current_size < best_size:
                            best_size = current_size
                            best_quality = q
                        else:
                            break
                    except Exception as e:
                        print(f"质量 {q} 临时保存出错: {str(e)}")
                        break

                final_save_args = {
                    'format': img_format, 'quality': best_quality, 'optimize': True
                }
                if img_format == 'JPEG': final_save_args['progressive'] = True
                if img_format == 'PNG': final_save_args['compress_level'] = 9
                img.save(output_path, **final_save_args)

                compressed_size = output_path.stat().st_size
                if original_size == 0:
                    ratio = 0
                else:
                    ratio = (compressed_size / original_size) * 100
                
                self.stats['original_size'] += original_size
                self.stats['compressed_size'] += compressed_size

                print(f"  压缩完成: {input_path.name}")
                print(f"  尺寸: {original_size / 1024:.1f}KB → {compressed_size / 1024:.1f}KB")
                print(f"  压缩率: {ratio:.1f}% | 最终质量: {best_quality}\n")
                return True

        except Exception as e:
            self.stats['failed'] += 1
            print(f"处理失败: {input_path}")
            print(f"  错误: {str(e)}\n")
            if output_path.exists():
                os.remove(output_path)
            return False

    def batch_compress(self, input_path: str, output_dir: str, quality: int, max_reduction: int,
                       overwrite: bool, recurse: bool, pattern: str):
        self.stats['start_time'] = time.time()
        
        input_p = Path(input_path).resolve()
        output_d = Path(output_dir).resolve()

        if not input_p.exists():
            print(f"输入路径不存在: {input_p}")
            return

        if input_p.is_file():
            files = [input_p]
        else:
            glob_pattern = f'**/{pattern}' if recurse else pattern
            files = [f for f in input_p.glob(glob_pattern) if f.is_file()]

        self.stats['total'] = len(files)
        if self.stats['total'] == 0:
            print(f"在 '{input_p}' 中未找到匹配 '{pattern}' 的文件")
            return

        print(f"发现 {self.stats['total']} 个待处理文件\n")
        output_d.mkdir(parents=True, exist_ok=True)

        for idx, file in enumerate(files, 1):
            if input_p.is_dir():
                relative_path = file.relative_to(input_p)
                output_path = output_d / relative_path
            else:
                output_path = output_d / file.name

            output_path.parent.mkdir(parents=True, exist_ok=True)

            print(f"处理中 ({idx}/{self.stats['total']}): {file}")
            
            if self.optimize_image(file, output_path, quality, max_reduction, overwrite):
                self.stats['processed'] += 1

        self._print_report()

    def _print_report(self):
        elapsed = time.time() - self.stats['start_time']
        print("\n" + "=" * 50)
        print("压缩报告")
        print("=" * 50)
        print(f"总文件数:   {self.stats['total']}")
        print(f"成功处理:   {self.stats['processed']}")
        print(f"跳过文件:   {self.stats['skipped']}")
        print(f"失败文件:   {self.stats['failed']}")

        if self.stats['processed'] > 0 and self.stats['original_size'] > 0:
            original_mb = self.stats['original_size'] / (1024 ** 2)
            compressed_mb = self.stats['compressed_size'] / (1024 ** 2)
            avg_ratio = (self.stats['compressed_size'] / self.stats['original_size']) * 100

            print(f"\n原始大小:  {original_mb:.2f} MB")
            print(f"压缩大小:  {compressed_mb:.2f} MB")
            print(f"平均压缩率: {avg_ratio:.1f}%")
            print(f"节省空间:  {original_mb - compressed_mb:.2f} MB")

        print(f"\n总耗时:    {elapsed:.1f}秒")
        print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="智能图片批量压缩工具 v2.2",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
使用示例:
  1. 压缩单个文件到 output 目录:
     python %(prog)s path/to/image.jpg -o output/

  2. 递归压缩 input_folder 内所有图片，初始质量为90:
     python %(prog)s input_folder/ -o output_folder/ -r -q 90

  3. 递归压缩 input_folder 内所有.png文件，并覆盖旧文件:
     python %(prog)s input_folder/ -o output_folder/ -r --overwrite --pattern "*.png"
"""
    )
    parser.add_argument("input", help="输入文件或目录的路径")
    parser.add_argument("-o", "--output", required=True, help="【必需】输出目录的路径")
    parser.add_argument("-q", "--quality", type=int, default=85, help="初始压缩质量 (1-95)，值越高图片质量越好，文件越大。默认: 85")
    parser.add_argument("-m", "--max-reduction", type=int, default=25, help="从初始质量开始的最大降幅，用于智能探测。默认: 25")
    parser.add_argument("-r", "--recurse", action="store_true", help="递归处理输入目录中的子目录")
    parser.add_argument("--overwrite", action="store_true", help="覆盖输出目录中已存在的文件")
    parser.add_argument("--pattern", default='*', help="要匹配的文件模式，如 '*.jpg' 或 'img_*.*'。默认: '*' (所有文件)")

    args = parser.parse_args()

    compressor = SmartImageCompressor()
    compressor.batch_compress(
        input_path=args.input,
        output_dir=args.output,
        quality=args.quality,
        max_reduction=args.max_reduction,
        overwrite=args.overwrite,
        recurse=args.recurse,
        pattern=args.pattern
    )

if __name__ == "__main__":
    main()