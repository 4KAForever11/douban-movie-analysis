### 项目简介

项目全程使用python开发，相对来说比较粗制滥造了

窗体使用pygame库开发

主要功能就是爬取豆瓣电影的指定详细页的评论，然后用爬到的评论使用训练好的情感分析模型进行输出分析正面评论和负面评论的数量

`analyze_comments.py`是pygame窗口需要调用的模块：我把爬虫和调用本地情感分析模型的功能都集成进去了

`window.py`是pygame的窗口代码：主要就是运行窗口控件调用`analyze_comments.py`里面的`analyze_movie`模块

`spider.py`是原来用来测试的爬虫的代码

因为没有弄好豆瓣的反爬，实质上现在`analyze_comments.py`的爬虫是不可用的状态，但原来的`spider.py`是可以使用的

<br>

### 注意事项

1. **依赖库**: 确保安装了所有需要的库和anaconda，包括`paddle`, `paddlenlp`, `pygame`, `pyperclip`，`emoji` 和 `beautifulsoup4`。其他基本不需要安装,除非你用的不是conda环境
   
2. **字体路径**: 检查字体路径是否正确。我用的msyh.ttc(微软雅黑)
   
3. **模型路径**: 确保模型的路径正确且模型已下载并准备好。模型已经训练好了
   
4. **运行环境**: 确保在适合的 Python 环境中运行,我使用的conda创建了一个python版本为3.9的虚拟环境

<br>

### 安装部署

**conda命令提示符**

创建名为douban-movie-analysis的conda虚拟环境，指定python版本为3.9

```bash
conda create -n douban-movie-analysis python=3.9

<br>

**激活conda虚拟环境douban-movie-analysis**
```bash
conda activate douban-movie-analysis

<br>

**pip一键下载需要的库**
确保命令行在项目路径下才能运行下面的命令
```Python
pip install -r requirements.txt


