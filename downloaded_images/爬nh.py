# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

def download(url,a,i):
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    save_dir = f'D://漫画/pic{a}'
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f'{i+1}.png')
    with open(file_path, 'wb') as f:
        f.write(response.content)

def main():
    url=input('下载地址：')
    a = int(input("你要下载到pic文件夹的序号是："))
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    }
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        base_pages = page.locator('//a[@class="gallerythumb"]/img').all()
        length = len(base_pages)
        base_url = []
        for base_page in base_pages:
            src=base_page.get_attribute('data-src')
            src = re.sub(r'(.*)(t\d.nhentai.net)', r'https://\2',src)
            src = re.sub(r'//t', '//i', src)
            src = re.sub(r'(\d+)t', r'\1', src)
            src = re.sub(r'\.webp\.webp$', '.webp', src)
            src = re.sub(r'\.jpg\.webp$', '.jpg', src)
            src = re.sub(r'(galleries/\d+)/(\d+)', r"\1/\2t", src)
            base_url.append(src)
        page.wait_for_timeout(20000)
    print(base_url)
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        for i in range(0, length):
            url = base_url[i]
            print(f'提交任务: 第{i+1}话')
            # 提交任务到线程池
            future = executor.submit(download, url, a, i)
            futures.append(future)
    print(f'总共{length}话')
    print('上一次下载的pic为：',a)

if __name__=='__main__':
    main()







