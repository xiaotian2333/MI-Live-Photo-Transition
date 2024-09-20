from PIL import Image
import re
import os
import sys

# 检查参数数量
if len(sys.argv) < 2:
    folder_path = input("请输入包含实况图文件夹的路径：")
else:
    # 获取参数
    folder_path = sys.argv[1]


# 遍历文件夹中的文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith('.jpg'):  # 检查文件扩展名
            full_path = os.path.join(root, file)
            # 去除后缀并取得文件名
            file_name_without_ext = os.path.splitext(file)[0]

            # 打开图像
            image = Image.open(full_path)

            # 读取 EXIF 数据
            exif_data = image._getexif()

            if exif_data:
                # 将 EXIF 数据转换为可读格式
                for tag_id, value in exif_data.items():
                    value = str(value)
                    if "MicroVideoOffset" in value:
                        break # 读取到就可以直接中断了

                # 正则表达式匹配
                pattern = r'MicroVideoOffset="(\d+)"'
                match = re.search(pattern, value)

                if match:
                    micro_video_offset = int(match.group(1)) # 图片结束，视频开始的字节
                else:
                    print("未找到标记视频大小的元数据")

                # 读取源文件的二进制数据
                with open(full_path, 'rb') as input_file:
                    # 将文件指针移动到末尾减去指定字节数的位置
                    input_file.seek(-micro_video_offset, os.SEEK_END)
                    # 读取从该位置到文件末尾的所有字节
                    data = input_file.read()

                # 将截取的数据写入目标文件
                with open(file_name_without_ext+".mp4", 'wb') as output_file:
                    output_file.write(data)

                print('截取的视频已写入到:', file_name_without_ext+".mp4")

            else:
                print("没有找到 EXIF 数据")