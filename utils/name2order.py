import os

# 遍历pic目录下的所有文件夹
def rename(pic_dir):
    for folder_name in os.listdir(pic_dir):
        folder_path = os.path.join(pic_dir, folder_name)
        if os.path.isdir(folder_path):  # 确保是文件夹
            for filename in os.listdir(folder_path):
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.PNG'):
                    old_file_path = os.path.join(folder_path, filename)
                    new_filename = f"{folder_name}_{filename}"
                    new_file_path = os.path.join(folder_path, new_filename)
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} -> {new_file_path}")


if __name__ == '__main__':
    pic_dir = '../../pic'  # pic目录路径
    rename(pic_dir)
