import requests
from bs4 import BeautifulSoup
import paddle
from paddlenlp.transformers import ErnieForSequenceClassification, ErnieTokenizer
from paddlenlp.data import Pad, Tuple
import emoji
import random
import time

# 加载情感分析模型和分词器
checkpoint_path = 'D:/douban-movie-analysis/aistudio/checkpoint'
model = ErnieForSequenceClassification.from_pretrained(checkpoint_path)
tokenizer = ErnieTokenizer.from_pretrained(checkpoint_path)
label_map = {0: 'negative', 1: 'positive'}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
]


def contains_emoji(text):
    """判断评论中是否包含表情符号"""
    return any(emoji.is_emoji(char) for char in text)


def fetch_comments_page(url):
    """抓取页面的 HTML 内容"""
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Referer': 'https://movie.douban.com/'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求出现异常: {e}")
        return None


def get_movie_comments(movie_id):
    """爬取多页评论内容"""
    comments = []
    for page in range(10):  # 爬取前10页评论
        start = page * 20
        url = f"https://movie.douban.com/subject/{movie_id}/comments?start={start}&limit=20&status=P&sort=new_score"
        print(f"正在爬取：{url}")

        html = fetch_comments_page(url)
        if not html:
            print(f"第 {page + 1} 页加载失败")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        for comment_tag in soup.find_all('span', class_='short'):
            text = comment_tag.get_text(strip=True)
            if not contains_emoji(text):
                comments.append(text)

        print(f"第 {page + 1} 页爬取成功，共爬取 {len(comments)} 条评论")
        time.sleep(random.uniform(5, 20))  # 随机延时，避免频繁请求

    return comments


def analyze_sentiment(comments):
    """对评论进行情感分析并返回情感标签列表"""
    model.eval()
    examples = [
        (
            tokenizer(comment, max_length=128, padding='max_length', truncation=True, return_dict=False)["input_ids"],
            tokenizer(comment, max_length=128, padding='max_length', truncation=True, return_dict=False)[
                "token_type_ids"]
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


def analyze_movie(movie_id):
    """获取多页短评并进行情感分析"""
    print("分析按钮已点击，正在分析...")
    comments = get_movie_comments(movie_id)
    if not comments:
        print("未能成功爬取任何评论")
        return 0, 0

    sentiments = analyze_sentiment(comments)
    positive_count = sentiments.count("positive")
    negative_count = sentiments.count("negative")
    return positive_count, negative_count


# # 使用示例：输入电影ID
# movie_id = input("请输入电影ID：")
# positive_count, negative_count = analyze_movie(movie_id)
# print(f"正面评论数：{positive_count}，负面评论数：{negative_count}")
