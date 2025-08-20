# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
import os
def download_image_one(url,a):
    headers={ "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)
        imgs=page.locator('//a[@style="margin-left: 1em; margin-right: 1em;"]/img').all()
        urls = [img.get_attribute('src') for img in imgs]  # 获取所有图片地址
        n = len(urls)
        print(f'共有{n}张图片，正在下载......')
        for i in range(1, n + 1):
            print(f"正在下载第{i}张图片......")
            if i == n:
                print('主人，已经被填满了~~~')
            save_dir = f'D://漫画/pic{a}'
            os.makedirs(save_dir, exist_ok=True)  # 自动创建目录
            file_path = os.path.join(save_dir, f'{i+count}.jpg')
            with open(file_path, 'wb') as f:
                f.write(requests.get(url='https://baramangaonline.com/'+urls[i - 1], headers=headers).content)
        page.close()

def download_image_more(url,a):
    headers={ "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto(url)
        page.wait_for_timeout(2000)
        imgs=page.locator('//a[@style="margin-left: 1em; margin-right: 1em;"]/img').all()
        urls=[img.get_attribute('src') for img in imgs]#获取所有图片地址
        n=len(urls)
        print(f'第{j+1}话共有{n}张图片，正在下载......')
        for i in range(1, n + 1):
            print(f"正在下载第{i}张图片......")
            if i == n:
                print('主人，已经被填满了~~~')
            save_dir = f'D://漫画/pic{a}'
            os.makedirs(save_dir, exist_ok=True)#自动创建目录
            file_path = os.path.join(save_dir, f'{i+count}.jpg')
            with open(file_path, 'wb') as f:
                f.write(requests.get(url='https://baramangaonline.com/'+urls[i-1],headers=headers).content)
        page.close()
    return n

if __name__ == '__main__':
    url = input('下载地址：')
    a=int(input("下载到pic文件夹的序号是："))
    m = int(input("共有几话："))
    count = 0
    if m == 1:
        download_image_one(url, a)
    elif m >= 2:
        x = len(url.split('-')[-1])
        url0 = url[:-x]
        url = [url0 + f'{i}/' for i in range(1, m + 1)]
        for j in range(0,m):
            count += download_image_more(url[j], a)
        print(f"总共下载了{count}张图片")
    else:
        print('话数错误')
