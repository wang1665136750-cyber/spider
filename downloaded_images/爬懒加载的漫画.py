# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
import os
import time
import random
def download(url,a):
    headers={ "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto(url)
        page.wait_for_timeout(2000)
        #鼠标滚动加载
        s = 0
        while True:
            v = random.randint(500, 1000)
            s = s + v
            page.mouse.wheel(delta_x=0, delta_y=v)
            # 获取当前页面内容的高度
            page_height = page.evaluate('() => document.documentElement.scrollHeight')
            print("当前页面内容的高度为", page_height)
            print("目前滚动的总高度为：", s)
            if s >= page_height - 1500:
                break
            page.wait_for_timeout(random.randint(200, 1500))
        print("已经滚动到了页面底部")
        imgs=page.locator('//img[@class="absimg"]').all()
        src=[img.get_attribute('src') for img in imgs]
        n=len(src)
        print(src)
        save_dir = f'D://漫画/pic{a}'
        os.makedirs(save_dir, exist_ok=True)  # 自动创建目录
        print(f'共有{n}张图片，正在下载......')
        for i in range(1,n+1):
            print(f"正在下载第{i}张图片......")
            if i == n:
                print('主人，已经被填满了~~~')
            file_path = os.path.join(save_dir, f'{i}.jpg')
            with open(file_path, 'wb') as f:
                f.write(requests.get(url=src[i - 1], headers=headers).content)
        page.wait_for_timeout(20000)
