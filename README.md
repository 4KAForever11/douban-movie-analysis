### 项目简介

项目全程使用`python`环境，版本`python-3.9.20`，开发IDE工具`PyCharm`，版本`PyCharm 2024.1(Professional Edition)`

窗体使用`pygame`库开发

主要功能就是爬取豆瓣电影的指定详细页的评论，然后用爬到的评论使用训练好的情感分析模型进行输出分析正面评论和负面评论的数量

目录：`D:\douban-movie-analysis\aistudio\checkpoint`里面是已经训练好了的一个情感分析模型

`analyze_comments.py`是pygame窗口需要调用的模块：我把爬虫和调用本地情感分析模型的功能都集成进去了

`window.py`是pygame的窗口代码：主要就是运行窗口控件调用`analyze_comments.py`里面的`analyze_movie`模块

`spider.py`是原来用来测试的爬虫的代码

使用`fake_useragent`库随机生成用户代理

<br>

### 注意事项

1. **依赖库**: 确保安装了所有需要的库和anaconda，包括`paddle`, `paddlenlp`, `pygame`, `pyperclip`，`emoji` ，`fake_useragent`和 `beautifulsoup4`。其他需要的库基本不需要安装,除非你用的不是conda环境
   
2. **字体路径**: 检查字体路径是否正确。我用的msyh.ttc(微软雅黑)
   
3. **模型路径**: 确保模型的路径正确且模型已下载并准备好。模型已经训练好了,需在[发行版](https://github.com/4KAForever11/douban-movie-analysis/releases)下载所有源码里面包含了模型
   
4. **运行环境**: 确保在适合的 Python 环境中运行,我使用的conda创建了一个python版本为3.9的虚拟环境

<br>

### 安装部署

在[发行版](https://github.com/4KAForever11/douban-movie-analysis/releases)下载源代码

**1. 创建 Conda 虚拟环境**

在 **conda命令提示符** 中创建名为 `douban-movie-analysis` 的 conda 虚拟环境，指定 Python 版本为 3.9：

```bash
conda create -n douban-movie-analysis python=3.9
```
<br>
2. 激活 Conda 虚拟环境

```bash
conda activate douban-movie-analysis
```
<br>
3. 运行以下命令下载所需的库：

```bash
pip install -r requirements.txt
```
<br>
4. 下载完成后，运行`window.py`

![pygame](tu/v0.2-pygame.png)

在输入框里面粘贴好豆瓣电影的某个电影的ID，比如一个电影的详细页网址是：https://movie.douban.com/subject/36296618/
那么`36296618`就是这个电影的ID

最后点分析按钮运行程序，如果爬虫能正常爬取到数据，那么他就会继续运行，本地情感分析可能需要一点时间出结果，耐心等待下即可。

下面就是运行出来分析ID为`36296618`的电影`志愿军：存亡之战`的分析结果,不过由于爬虫能力的限制只爬到了6页评论，所以也就只分析了6页的评论😀

![pygame-run](tu/v0.2-pygame-run.png)

下面是python在运行的过程截图

![code-run](tu/v0.2-run.png)

### 程序运行的流程

**1. pygame的窗体**

**2. 加载本地情感分析模型**

**3. 等待用户输入网址**

**4. 等待用户点击分析按钮**

**5. 传入用户输入的网址**

**6. 运行爬虫爬取评论**

**7. 保存爬取到的评论**

**8. 调用情感分析模型进行分析**

**9. 返回结果给pygame窗体并显示**
