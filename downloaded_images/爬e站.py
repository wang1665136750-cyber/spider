# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
import re
def download_img(url,a,i):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
        }
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    pic_url = html.xpath('//img[@id="img"]/@src')[0]
    print(response.status_code)
    pic=requests.get(url=pic_url,headers=headers).content
    save_dir = f'D://漫画/pic{a}'
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f'{i+1}.png')
    with open(file_path, 'wb') as f:
        f.write(pic)
def main():
    url0=input('下载地址：')
    a = int(input("你要下载到pic文件夹的序号是:"))
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url0)
        base_url = []
        src_s = page.locator('//div[@id="gdt"]//a').all()
        for src in src_s:
            base_url.append(src.get_attribute('href'))
        info = page.locator('//tr//td[@onclick]/a')
        if len(info.all())>0:
            old_length = len(info.all())
            length = page.locator('//tr//td[@onclick]/a').nth(int(old_length / 2 - 2)).all_inner_texts()[0]
            length = int(length)
            for i in range(int(length-1)):
                url=url0+f'?p={i+1}'
                page.goto(url)
                src_s = page.locator('//div[@id="gdt"]//a').all()
                for src in src_s:
                    base_url.append(src.get_attribute('href'))
        length=len(base_url)
        print(base_url)
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        for i in range(0, length):
            img_url = base_url[i]
            print(f'提交任务: 第{i+1}话')
            # 提交任务到线程池
            future = executor.submit(download_img, img_url, a, i)
            futures.append(future)
    print(f'总共{length}话')
    print('上一次下载的pic为：', a)


if __name__=='__main__':
    main()
