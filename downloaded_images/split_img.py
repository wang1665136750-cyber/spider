from PIL import Image
import os
import math
def split_image_with_remainder(input_path, rows, cols, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    count = 0
    input_path_list=os.listdir(input_path)
    input_path_list=sorted(input_path_list, key=lambda x: int(os.path.splitext(x)[0]))
    for img in input_path_list:
        img=os.path.join(input_path,img)
        img = Image.open(img)
        width, height = img.size
        # 计算每个小块的理想尺寸
        tile_width = math.ceil(width / cols)
        tile_height = math.ceil(height / rows)
        for i in range(rows):
            for j in range(cols):
                # 计算当前小块的实际边界
                left = j * tile_width
                upper = i * tile_height
                right = min((j + 1) * tile_width, width)
                lower = min((i + 1) * tile_height, height)
                if right <= left or lower <= upper:
                    continue
                tile = img.crop((left, upper, right, lower))
                tile.save(os.path.join(output_dir, f"{count+1}.jpg"))
                count += 1

input_path=input("初始路径:").strip('"')
out_put=input('输出路径:').strip('"')
split_image_with_remainder(input_path=input_path, rows=7, cols=1, output_dir=out_put)