# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
import os
import re
def download_image(url,a):
    headers={"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page()
        page.goto(url)
        page.wait_for_timeout(2000)
        img_container=page.query_selector_all('//div[@id="container"]//p[child::img]')
        urls=[]
        for img in img_container:
            img_element=img.query_selector('img')
            if img_element:
                srcset_attr = img_element.get_attribute('srcset')
                for srcset in srcset_attr:
                    srcset_items = srcset_attr.split(',')
                for items in srcset_items:
                    src=items.strip().split()[0]
                    if 'x1024' in src and '.jpg' in src:
                        urls.append(src)

        n=len(urls)
        print(f'开始下载{n}张照片')
        for i in range(1,n+1):
            print(f"正在下载第{i}张照片......")
            if i==n:
                print(f'下载完毕')
            save_dir=f'D://漫画/pic{a}'
            os.makedirs(save_dir,exist_ok=True)
            file_path=os.path.join(save_dir,f'{i}.png')
            with open(file_path,'wb') as f:
                    f.write(requests.get(urls[i-1],headers=headers).content)
        page.close()

if __name__=='__main__':
    url = input('下载链接:')
    a = int(input("你要下载到pic文件夹的序号是："))
    download_image(url, a)

