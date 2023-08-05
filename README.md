# Signs

整理腾讯在线收集表的签名。（适用于班级远程签字）

1. 导出在线收集表
2. `extract_images.py`
3. `merge_into_a_column.py`
4. `sign_document.py`

所需文件请参考每段程序`if __name__ == "__main__":`后的定义。

```mermaid
flowchart TB
   在线收集表([在线收集表]) -->|"签名照片收集（收集结果）.xlsx"| extract_images
   在线收集表
      -->|"附件下载_签名照片收集.zip"| extract_images
      -->|"out/{name}.png"| merge_into_a_column
      -->|"out/merged.png"| sign_document

    names([名单<br>names.txt]) --> merge_into_a_column

    original([原始 PDF<br><small>大类分流毕业专业确认统计表</small>])
       --> sign_document
       --> signed([签了名的 PDF])
```

## 导出在线收集表

### 数据及签名

1. 访问腾讯在线收集表统计页面（`https://docs.qq.com/form/page/<id>#/result`），关联表格为“智能表”（与“工作表”相对）。
2. 打开表格，（右上角）文档操作 → 导出 → 本地 Excel 表格。
3. “文档中含有附件，将随文档一起导出，确认导出吗？”仅导出文档。
4. 用 Excel 打开下载下来的文件，重新保存。（原文件包含不合法的 XML）

此表格B–D列依次为名称、图像（文件名）、签名。

### 图像

1. 访问腾讯在线收集表统计页面，照片题目 → 下载此题的全部文件。
2. “请选择下载方式”？默认下载，确定。

## 设计指导思想

[![xkcd 1205: Is It Worth the Time?](https://imgs.xkcd.com/comics/is_it_worth_the_time.png "Don't forget the time you spend finding the chart to look up what you save. And the time spent reading this reminder about the time spent. And the time trying to figure out if either of those actually make sense. Remember, every second counts toward your life total, including these right now.")](https://xkcd.com/1205/)
