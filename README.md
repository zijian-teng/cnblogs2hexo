# 批量下载博客园 md 文章

最近在搭建 Hexo 静态博客，需要把之前博客园的文章搬运过来。

博客园的 VS Code 插件支持下载 md 文章，但需要开通会员才可以批量下载全部文章。
不过博客园提供了备份功能，可以导出 sqlite/json/xml(rss) 格式的备份。唯一的遗憾是导出的备份不含分类和 tags 信息。

## 步骤

> ⚠️ 警告：操作前请先备份！！！

1. 在博客后台的“备份/导出”页面，选择“+创建备份”，等待几分钟，导出完成后，下载 SQLite 文件
2. 将 SQLite 的 db 文件（如 cnblogs_blog_tengzijian.20231111084303.db）拷贝到当前目录，执行 `./cnblogs_sqlite2md.py cnblogs_blog_tengzijian.20231111084303.db`，脚本运行结束后会打印统计信息，并按照是否博客是否公开存放在 export/_drafts 和 export/_posts 两个目录下
3. 【可选步骤】博客园导出的备份不含分类和标签信息，如果想对文章进行分类，可以在 export/_posts 目录下创建几个目录（支持子目录嵌套），把 md 文件移动到各自的目录，然后运行 './update_categories.py' 脚本即可。该脚本会将 export/_posts 目录下的所有 md 文件按照其所在的子目录自动更新目录信息，并拷贝到 export_with_category/_posts 目录

## Known Issues

1. 如果标题中含有英文":"，hexo 生成文章时会有警告

> ❤️ With the help of ChatGPT