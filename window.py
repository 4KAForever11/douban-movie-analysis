import pygame
import sys
import pyperclip  # 用于处理剪贴板内容
from analyze_comments import analyze_movie  # 导入爬虫和分析模块

# 初始化 pygame
pygame.init()

# 设置窗口大小和标题
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("豆瓣电影评论分析")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 204)
GRAY = (200, 200, 200)  # 用于输入提示文字颜色

# 加载支持中文的字体
font_path = "C:/Windows/Fonts/msyh.ttc"  # 字体路径，请根据实际情况修改
font = pygame.font.Font(font_path, 24)  # 设置字体大小

# 文本框和按钮位置定义
title_box = pygame.Rect(50, 30, 300, 40)
input_prompt_box = pygame.Rect(50, 100, 300, 32)
input_box = pygame.Rect(50, 150, 300, 32)
button_box = pygame.Rect(150, 200, 100, 40)
result_box = pygame.Rect(50, 280, 300, 150)

# 输入和结果变量
movie_id = ''
result_text = "分析结果："
input_active = False  # 输入框是否激活
input_placeholder = "请输入电影 ID"  # 输入提示文字
max_input_length = 10  # 限制输入框最大字符长度

# 主循环
running = True
while running:
    screen.fill(WHITE)

    # 绘制标题
    title_text = font.render("豆瓣电影评论分析", True, BLACK)
    screen.blit(title_text, (title_box.x + 40, title_box.y + 5))

    # 绘制“需要分析的电影 ID”提示
    prompt_text = font.render("需要分析的电影 ID", True, BLACK)
    screen.blit(prompt_text, (input_prompt_box.x, input_prompt_box.y))

    # 绘制输入框
    pygame.draw.rect(screen, BLACK if input_active else GRAY, input_box, 2)  # 增加边框颜色
    if movie_id:
        input_surface = font.render(movie_id, True, BLACK)
    else:
        input_surface = font.render(input_placeholder, True, GRAY)  # 显示提示文字
    screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

    # 绘制分析按钮
    pygame.draw.rect(screen, YELLOW, button_box)
    button_text = font.render("分析", True, BLACK)
    screen.blit(button_text, (button_box.x + 15, button_box.y + 5))

    # 绘制结果框
    pygame.draw.rect(screen, WHITE, result_box, 2)
    result_surface = font.render(result_text, True, BLACK)
    screen.blit(result_surface, (result_box.x + 5, result_box.y + 5))

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标点击是否在输入框上
            if input_box.collidepoint(event.pos):
                input_active = True  # 激活输入框
                if movie_id == input_placeholder:
                    movie_id = ''  # 清空提示文字
            else:
                input_active = False  # 未点击输入框则取消激活
            # 如果点击的是分析按钮
            if button_box.collidepoint(event.pos):
                print("分析按钮已点击，正在分析...")  # 打印调试信息
                print("输入的电影 ID:", movie_id)  # 确认ID内容
                if movie_id.isdigit():
                    # 调用分析模块进行情感分析
                    positive_count, negative_count = analyze_movie(movie_id)
                    result_text = f"正面评论: {positive_count} 负面评论: {negative_count}"
                else:
                    result_text = "请输入有效的电影 ID！"  # 提示格式错误
        elif event.type == pygame.KEYDOWN:
            if input_active:
                # 支持粘贴功能（Ctrl + V）
                if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    movie_id = pyperclip.paste()[:max_input_length]  # 从剪贴板粘贴内容并限制长度
                elif event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:  # 按下 Ctrl + Backspace 快速清空输入框
                        movie_id = ''
                    else:
                        movie_id = movie_id[:-1]
                elif event.unicode.isprintable() and len(movie_id) < max_input_length:  # 检查是否为可打印字符并限制长度
                    movie_id += event.unicode

    # 刷新屏幕
    pygame.display.flip()

pygame.quit()
sys.exit()
