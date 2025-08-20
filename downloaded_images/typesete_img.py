import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import importlib
import subprocess
import sys
def install_if_missing(package, import_name=None):
    """自动安装缺失的Python包"""
    try:
        importlib.import_module(import_name or package)
        print(f"模块 {import_name or package} 已存在。")
    except ImportError:
        print(f"正在安装 {package}...")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', package,
            '-i', 'https://mirrors.aliyun.com/pypi/simple/'
        ])
        print(f"{package} 安装完成。")
# 确保所需包已安装
install_if_missing('pandas')
install_if_missing('Pillow', 'PIL')
install_if_missing('openpyxl')  # 处理Excel
def draw_image_xhs(quote, author, img_path, font_path, output_folder,
                   layout="left", main_color="#000000", author_color="#555555",
                   bottom_margin=150, line_spacing=20):
    """
    生成小红书风格文字图片
    :param layout: "left" 左对齐, "center" 居中对齐
    """
    img = Image.open(img_path)
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    img_width, img_height = img.size
    font_main = ImageFont.truetype(font_path, 80)
    font_author = ImageFont.truetype(font_path, 60)
    draw = ImageDraw.Draw(img)
    # 自动换行
    margin_x = int(img_width * 0.1)
    max_text_width = img_width - 2 * margin_x
    lines = []
    line = ""
    for w in quote:
        test_line = line + w
        if draw.textlength(test_line, font=font_main) <= max_text_width:
            line = test_line
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    # 行高
    try:
        bbox = font_main.getbbox("A")
        line_height = bbox[3] - bbox[1] + line_spacing
    except AttributeError:
        line_height = font_main.getsize("A")[1] + line_spacing

    total_text_height = line_height * len(lines)
    author_height = font_author.getbbox("A")[3] - font_author.getbbox("A")[1]
    # 主文字起始 y
    start_y = img_height - bottom_margin - author_height - total_text_height
    # 绘制主文字
    for i, line in enumerate(lines):
        if layout == "center":
            text_width = draw.textlength(line, font=font_main)
            x = (img_width - text_width) // 2
        else:
            x = margin_x
        y = start_y + i * line_height
        draw.text((x, y), line, fill=main_color, font=font_main)
    # 绘制作者
    author_text = f"——{author}"
    if layout == "center":
        author_width = draw.textlength(author_text, font=font_author)
        author_x = (img_width - author_width) // 2
    else:
        author_x = margin_x
    author_y = img_height - bottom_margin
    draw.text((author_x, author_y), author_text, fill=author_color, font=font_author)
    # 保存
    os.makedirs(output_folder, exist_ok=True)
    safe_quote = ''.join(c for c in quote[:20] if c.isalnum() or c in " _-") or "quote"
    safe_author = ''.join(c for c in author if c.isalnum() or c in " _-") or "author"
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    output_filename = f"{base_name}_{safe_quote}_{safe_author}.jpg"
    output_path = os.path.join(output_folder, output_filename)
    img.save(output_path)
    print(f"已生成: {output_path}")
    return output_path
def process_images(input_path, font_path, excel_path, output_folder,
                   layout="left", main_color="#000000", author_color="#555555",
                   bottom_margin=150, line_spacing=20):
    """批量处理所有图片"""
    try:
        df = pd.read_excel(excel_path)
        quotes = df.iloc[1:, 0].tolist()
        authors = df.iloc[1:, 1].tolist()
        print(f"从Excel读取到 {len(quotes)} 条格言")
    except Exception as e:
        print(f"读取Excel失败: {e}")
        return
    # 获取图片列表
    image_paths = []
    if os.path.isfile(input_path) and input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        image_paths = [input_path]
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image_paths.append(os.path.join(input_path, file))

    print(f"找到 {len(image_paths)} 张图片")
    if len(image_paths) != len(quotes):
        print(f"警告: 图片数量({len(image_paths)})与格言数量({len(quotes)})不一致")
    num_to_process = min(len(image_paths), len(quotes))
    results = []
    for i in range(num_to_process):
        try:
            output_path = draw_image_xhs(
                str(quotes[i]), str(authors[i]),
                image_paths[i], font_path, output_folder,
                layout=layout, main_color=main_color, author_color=author_color,
                bottom_margin=bottom_margin, line_spacing=line_spacing
            )
            results.append(output_path)
        except Exception as e:
            print(f"处理失败: {image_paths[i]}, {quotes[i]} - {e}")
    print(f"\n处理完成! 共生成 {len(results)} 张图片")
    return results
if __name__ == "__main__":
    input_path = r"C:\Users\ylher\Downloads\tp"
    font_path = r"C:\Users\ylher\Downloads\SourceHanSansSC-Regular-2.otf"
    excel_path = r"C:\Users\ylher\Downloads\卡片文本.xlsx"
    output_folder = r"C:\Users\ylher\Downloads\1"

    process_images(
        input_path, font_path, excel_path, output_folder,
        layout="center",            # "left" 左对齐，"center" 居中
        main_color="#FFFFFF",       # 主文字颜色
        author_color="#333333",     # 作者颜色
        bottom_margin=150,          # 底部留白
        line_spacing=25             # 行间距
    )
