# -------------------------------------------------------------------------------
# Copyright (c) 2024. OTC, Inc. All Rights Reserved
# @作者 : OTC
# @邮件 : avotcorg@gmail.com
# @文件 : avotcorg - yxcfip.py
# @创建时间 : 2024/02/21 10:08
# -------------------------------------------------------------------------------
import requests
import re
import subprocess
import time
import os

def commit_and_push_to_github():
    # 从 Secrets 中获取访问令牌
    access_token = os.environ['url']

    # 设置 Git 的身份验证信息
    os.system(f'git config --global user.email "you@example.com"')
    os.system(f'git config --global user.name "Your Name"')
    os.system(f'git config --global credential.helper store')

    # 添加更改、提交更改和推送更改
    os.system('git add ip.txt cfip.txt')
    os.system(f'git commit -m "Update ip.txt and cfip.txt"')
    os.system(f'git push https://{access_token}@github.com/username/repository.git main')

url = os.environ['url']
response = requests.get(url)
html_content = response.text

ip_addresses = re.findall(r'<tg-spoiler>(\d+\.\d+\.\d+\.\d+)</tg-spoiler>', html_content)
ports = re.findall(r'<tg-spoiler>(\d+)</tg-spoiler>', html_content)
regions = re.findall(r'</i>(.+?)<br/><br/><b>\[IP\]</b>', html_content)
dates = re.findall(r'\[Date\]</b> (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) CST</div>', html_content)

with open('ip.txt', 'r', encoding='utf-8') as file1:
    existing_dates = {line.split(': ')[1].strip() for line in file1 if 'Date' in line}
with open('cfip.txt', 'r') as file1:
    existing_entries = {line.strip() for line in file1}

with open('ip.txt', 'a', encoding='utf-8') as file1, open('cfip.txt', 'a') as file2:
    for ip, port, region, date in zip(ip_addresses, ports, regions, dates):
        if date not in existing_dates:
            start_time = time.time()
            result = subprocess.run(['ping', '-c', '1', f'{ip}:{port}'], stdout=subprocess.PIPE).stdout.decode('utf-8', errors='ignore')
            end_time = time.time()
            ping_delay = round((end_time - start_time) * 1000, 2)
            if ping_delay > 0:
                print(f"Ping延时: {ping_delay}毫秒")
                print(result)
                file1.write(f"Ping延时: {ping_delay}毫秒\n")
                file1.write(result + '\n')
            file1.write(f"IP Address: {ip}\n")
            file1.write(f"Port: {port}\n")
            if region == 'CN' or region == '45102':
                region = 'HK'
            file1.write(f"Region: {region}\n")
            file1.write(f"Date: {date}\n\n")

            formatted_entry = f"{ip}:{port}#🔒{region}-TG频道@Warp_Key" if region != 'HK' else f"{ip}:{port}#🔒HK-TG频道@Warp_Key"
            file2.write(formatted_entry + '\n')

            print(f"IP Address: {ip}")
            print(f"Port: {port}")
            print(f"Region: {region}")
            print(f"Date: {date}")
            print('-----------------')

print("数据已经保存到 ip.txt 和 cfip.txt")
commit_and_push_to_github()
