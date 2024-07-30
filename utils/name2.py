import os
import argparse


def rename_images(folder_path):
    # 遍历文件夹中的子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前子文件夹中的图片文件
        for i, file in enumerate(files):
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                extension = os.path.splitext(file)[1]
                new_name = f"{i + 1}{extension}"
                new_path = os.path.join(root, new_name)
                old_path = os.path.join(root, file)
                os.rename(old_path, new_path)
                print(f"Renamed {file} to {new_name}")
    print('ok')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='./pic', help='the source of file')
    # parser.add_argument('--output', default='', help='output')
    arg = parser.parse_args()
    rename_images(arg.source)