#!/usr/bin/python3

import os
import sqlite3
from datetime import datetime
import re
import html
import sys

def main():
    if len(sys.argv) < 2:
        print(f'Please specify the sqlite db file. For example:\n\t{sys.argv[0]} cnblogs_blog_tengzijian.20231111084303.db')
        return

    # 数据库连接和查询
    conn = sqlite3.connect(sys.argv[1])
    cursor = conn.cursor()
    cursor.execute('SELECT Id, Title, DateAdded, DateUpdated, Body, AccessPermission FROM blog_Content')
    results = cursor.fetchall()

    # 创建存放 Markdown 文件的目录
    output_directory = 'export'
    draft_directory = os.path.join(output_directory, '_drafts')
    post_directory = os.path.join(output_directory, '_posts')

    # 检查并创建目录
    os.makedirs(draft_directory, exist_ok=True)
    os.makedirs(post_directory, exist_ok=True)

    # 统计文件数量
    draft_count = 0
    post_count = 0

    # 生成 Markdown 文件并统计
    for result in results:
        Id, Title, DateAdded, DateUpdated, Body, AccessPermission = result
        date = datetime.strptime(DateAdded, '%Y-%m-%d %H:%M:%S')
        updated = datetime.strptime(DateUpdated, '%Y-%m-%d %H:%M:%S')
        Title = html.unescape(Title)

        markdown_content = f'''---
    title: {Title}
    date: {date.strftime('%Y-%m-%d %H:%M:%S')}
    updated: {updated.strftime('%Y-%m-%d %H:%M:%S')}
    abbrlink: {Id}
    tags:
    categories:
    ---
    {Body}
    '''

        # 替换非法字符
        valid_title = re.sub(r'[\/:*?"<>|]', '_', Title)

        # 决定存放目录
        if AccessPermission == 'OwnerByUser':
            output_path = os.path.join(draft_directory, f'{valid_title}.md')
            draft_count += 1
        else:
            output_path = os.path.join(post_directory, f'{valid_title}.md')
            post_count += 1

        # 写入 Markdown 文件
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

    # 关闭数据库连接
    conn.close()

    # 打印统计结果
    print(f'Total drafts created: {draft_count}')
    print(f'Total posts created: {post_count}')

if __name__== "__main__":
    main()