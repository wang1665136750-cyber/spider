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
        page.wait_for_timeout(2000)
        imgs=page.locator('//*[@class="row col-lg-12 col-md-12 col-xs-12" and ./img]/img')#指定包含图片的class标签
        urls=[img.get_attribute('src') for img in imgs.all()]#获取所有图片地址
        n=len(urls)
        print(f'共有{n}张图片，正在下载......')
        for i in range(1, n + 1):
            print(f"正在下载第{i}张图片......")
            if i == n:
                print('主人，已经被填满了~~~')
            save_dir = f'D://漫画/pic{a}'
            os.makedirs(save_dir, exist_ok=True)#自动创建目录
            file_path = os.path.join(save_dir, f'{i}.jpg')
            with open(file_path, 'wb') as f:
                f.write(requests.get(url=urls[i-1],headers=headers).content)
        page.wait_for_timeout(20000)

def download_image_more(url,a):
    headers={ "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page()
        page.goto(url)
        page.wait_for_timeout(2000)
        imgs=page.locator('//*[@class="row col-lg-12 col-md-12 col-xs-12" and ./img]/img')#指定包含图片的class标签
        urls=[img.get_attribute('src') for img in imgs.all()]#获取所有图片地址
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
                f.write(requests.get(url=urls[i-1],headers=headers).content)
        page.wait_for_timeout(20000)
    return n

if __name__ == '__main__':
    m = int(input("共有几话："))
    url = input('下载链接:')
    a = int(input("你要下载到pic文件夹的序号是："))
    if m == 1:
        download_image_one(url, a)
    elif m >= 2:
        count = 0
        url0 = url[:-1]
        url = [url0 + f'{i}' for i in range(1, m + 1)]
        for j in range(m):
            count += download_image_more(url[j], a)
        print(f"总共下载了{count}张图片")
    else:
        print('话数错误')


