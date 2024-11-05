import requests
import time
import random
import re
from bs4 import BeautifulSoup
import paddle
from paddlenlp.transformers import ErnieForSequenceClassification, ErnieTokenizer
from paddlenlp.data import Pad, Tuple
import emoji

# 加载情感分析模型和分词器
checkpoint_path = 'D:/douban-movie-analysis/aistudio/checkpoint'
model = ErnieForSequenceClassification.from_pretrained(checkpoint_path)
tokenizer = ErnieTokenizer.from_pretrained(checkpoint_path)
label_map = {0: 'negative', 1: 'positive'}

def contains_emoji(text):
    """判断评论中是否包含表情符号"""
    return any(emoji.is_emoji(char) for char in text)

def fetch_page(url, headers):
    """获取页面的函数，加入重试机制"""
    for attempt in range(3):  # 尝试3次
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except requests.RequestException as e:
            print(f"请求出现异常: {e}")
        time.sleep(random.uniform(3, 10))  # 每次失败后等待随机时间
    return None  # 如果3次都失败，返回None

def get_movie_comments(url):
    """从豆瓣电影页面爬取前10页的评论并返回评论列表"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    movie_id = re.search(r'\d+', url).group()
    comment_url_template = f"https://movie.douban.com/subject/{movie_id}/comments?start={{}}&limit=20&status=P"
    all_comments = []

    for page in range(10):  # 前10页评论
        start = page * 20
        comment_url = comment_url_template.format(start)
        response = fetch_page(comment_url, headers)

        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            comment_elements = soup.find_all('span', class_='short')

            for comment in comment_elements:
                text = comment.get_text(strip=True)
                if not contains_emoji(text):  # 过滤掉包含表情符号的评论
                    all_comments.append(text)
            print(f"第 {page + 1} 页爬取成功")
        else:
            print(f"第 {page + 1} 页爬取失败")

        time.sleep(random.uniform(1, 3))  # 增加随机延时

    return all_comments

def analyze_sentiment(comments):
    """对评论进行情感分析并返回情感标签列表"""
    model.eval()
    examples = [
        (
            tokenizer(comment, max_length=128, padding='max_length', truncation=True, return_dict=False)["input_ids"],
            tokenizer(comment, max_length=128, padding='max_length', truncation=True, return_dict=False)["token_type_ids"]
        )
        for comment in comments
    ]

    batchify_fn = lambda samples, fn=Tuple(
        Pad(axis=0, pad_val=tokenizer.pad_token_id),
        Pad(axis=0, pad_val=tokenizer.pad_token_type_id)
    ): fn(samples)

    data_loader = paddle.io.DataLoader(
        dataset=examples,
        batch_size=1,
        collate_fn=batchify_fn,
        return_list=True
    )

    results = []
    for batch in data_loader:
        input_ids, token_type_ids = batch
        logits = model(input_ids, token_type_ids)
        probs = paddle.nn.functional.softmax(logits, axis=1).numpy()
        preds = probs.argmax(axis=1)
        results.extend([label_map[pred] for pred in preds])

    return results

def analyze_movie(url):
    """爬取评论并进行情感分析"""
    print("分析按钮已点击，正在分析...")
    comments = get_movie_comments(url)
    if not comments:
        print("未能成功爬取任何评论")
        return 0, 0

    sentiments = analyze_sentiment(comments)
    positive_count = sentiments.count("positive")
    negative_count = sentiments.count("negative")
    return positive_count, negative_count
