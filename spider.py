import requests
from bs4 import BeautifulSoup
import re
import time
import emoji

def contains_emoji(text):
    """判断评论中是否包含表情符号"""
    return any(emoji.is_emoji(char) for char in text)

def get_movie_comments(url):
    # 提取电影 ID
    movie_id = re.search(r'\d+', url).group()
    # 评论的基准 URL
    comment_url_template = f"https://movie.douban.com/subject/{movie_id}/comments?start={{}}&limit=20&status=P"

    # 存储评论
    all_comments = []

    # 遍历前 10 页
    for page in range(10):
        start = page * 20  # 每页有 20 条评论
        comment_url = comment_url_template.format(start)
        print(f"正在爬取第 {page + 1} 页评论...")

        # 获取页面内容
        response = requests.get(comment_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"无法访问评论页面，第 {page + 1} 页跳过")
            continue

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.find_all('span', class_='short')

        # 提取、过滤并存储评论
        for comment in comments:
            text = comment.get_text(strip=True)
            if not contains_emoji(text):  # 如果不包含表情符号，则保存
                all_comments.append(text)
                print(text)  # 打印评论

        # 防止过快爬取，加入延迟
        time.sleep(1)

    # 保存评论到文本文件
    with open("douban_comments.txt", "w", encoding="utf-8") as file:
        for comment in all_comments:
            file.write(comment + "\n")
    print("评论已保存到 douban_comments.txt 文件中")

# 示例调用
url = input("请输入豆瓣电影的详细页 URL: ")
get_movie_comments(url)
