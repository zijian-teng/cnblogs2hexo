#!/usr/bin/python3

import os
import shutil
import re

def safe_rmtree(directory):
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass

def update_categories(md_path, base_path):
    # 获取相对路径
    rel_path = os.path.relpath(md_path, base_path)

    # 分割路径
    categories = rel_path.split(os.path.sep)
    categories = categories[:-1]

    # 更新 md 文件中的 categories
    with open(md_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip() == 'categories:':
            lines[i + 1] = '  ' + '\n  '.join(f'- {category}' for category in categories) + '\n---\n'
            break

    with open(md_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def copy_to_categorized(source_dir, dest_dir):
    tmp_dir = source_dir + "_tmp"
    safe_rmtree(tmp_dir)
    shutil.copytree(source_dir, tmp_dir)
    source_dir=tmp_dir

    os.makedirs(dest_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                update_categories(md_path, source_dir)

                # 拷贝文件到 _post_categorized 目录
                shutil.copy(md_path, dest_dir)

    shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    source_directory = 'export/_posts'
    destination_directory = 'export_with_category/_posts'

    # 调用拷贝和更新函数
    copy_to_categorized(source_directory, destination_directory)

    print(f"Categories updated and files copied to {destination_directory} directory.")
