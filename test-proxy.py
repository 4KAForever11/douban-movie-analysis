import requests


def test_proxy(proxy):
    """测试代理是否有效"""
    url = "http://httpbin.org/ip"  # 测试代理的公共API，返回请求IP地址
    proxies = {
        "http":'35.79.120.242:3128',
        "https":'35.79.120.242:3128',
        "http":'20.205.61.143:80',
        "https": '20.205.61.143:80',
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=10)  # 设置超时为10秒
        if response.status_code == 200:
            print(f"代理 {proxy} 正常工作。响应内容: {response.json()}")
        else:
            print(f"代理 {proxy} 请求失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"代理 {proxy} 无法连接，错误: {e}")


# 测试代理
test_proxy("https://20.205.61.143:80")  # 用你要测试的代理替换
