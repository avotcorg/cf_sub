# -------------------------------------------------------------------------------
# Copyright (c) 2024. OTC, Inc. All Rights Reserved
# @作者         : OTC
# @邮件         : avotcorg@gmail.com
# @文件         : avotcorg - yxcfip.py
# @创建时间     : 2024/02/21 10:08
# -------------------------------------------------------------------------------
import requests
import re
import os

url = os.environ['url']
response = requests.get(url)
html_content = response.text

ip_addresses = re.findall(r'<tg-spoiler>(\d+\.\d+\.\d+\.\d+)</tg-spoiler>', html_content)
ports = re.findall(r'<tg-spoiler>(\d+)</tg-spoiler>', html_content)
regions = re.findall(r'\[Region\]</b>\s(.+?)<br/>', html_content)
dates = re.findall(r'\[Date\]</b> (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) CST</div>', html_content)

with open('ip.txt', 'r') as file1:
    existing_dates = {line.split(': ')[1].strip() for line in file1 if 'Date' in line}
with open('cfip.txt', 'r') as file1:
    existing_entries = {line.strip() for line in file1}

with open('ip.txt', 'a') as file1, open('cfip.txt', 'a') as file2:
    for ip, port, region, date in zip(ip_addresses, ports, regions, dates):
        if date not in existing_dates:
            file1.write(f"IP Address: {ip}\n")
            file1.write(f"Port: {port}\n")
            if region == 'CN' or region == '45102':
                region = 'HK'
            file1.write(f"Region: {region}\n")
            file1.write(f"Date: {date}\n\n")

            formatted_entry = f"{ip}:{port}#{region}" if region != 'HK' else f"{ip}:{port}#HK"
            file2.write(formatted_entry + '\n')

            print(f"IP Address: {ip}")
            print(f"Port: {port}")
            print(f"Region: {region}")
            print(f"Date: {date}")

print("数据已经保存到 ip.txt 和 cfip.txt")
