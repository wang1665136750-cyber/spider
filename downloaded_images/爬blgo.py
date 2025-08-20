# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor
def download_image(url,save_dir,i):
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    file_path=os.path.join(save_dir,f'{i}.png')
    with open(file_path,'wb') as f:
            f.write(requests.get(url,headers=headers).content)

def main(url,a):
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(2000)
        img_container = page.locator('//div[@id="post-hentai"]//img').all()
        urls = []
        for img in img_container:
            src = img.get_attribute('src')
            urls.append(src)
        n = len(urls)
        page.close()
    with ThreadPoolExecutor(max_workers=n) as executor:
        futures=[]
        for i in range(1,n+1):
            save_dir = f'D://漫画/pic{a}'
            os.makedirs(save_dir, exist_ok=True)
            base_url = urls[i-1]
            print(f'提交任务: 第{i}话')
            future = executor.submit(download_image,base_url,save_dir, i)
            futures.append(future)
        print(f'总共{n}话')
        print('上一次下载的pic为：', a)

if __name__=='__main__':
    url = input('下载链接:')
    a = int(input("你要下载到pic文件夹的序号是："))
    main(url, a)

