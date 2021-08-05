# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs


def main():
    txt_path = r"./idioms.txt"
    url_basic = r"http://chengyu.t086.com"
    idiom = {}
    for alpha in [chr(65 + i) for i in range(26)]:
        idiom[alpha], p = [], 1
        while True:
            url = f"{url_basic}/list/{alpha}_{p}.html"
            try:
                res = requests.get(url)
                if res.status_code != 200:
                    break
                page = bs(res.content, "lxml")
                for pg in page.select("div.listw ul li a"):
                    idiom[alpha].append(str(pg.string))
            except Exception as e:
                print(e)
            p += 1
        print(f"\rrunning in page {alpha}.", end='')
    with open(txt_path, "w", encoding="utf-8") as f:
        for key, value in idiom.items():
            f.write(key + '\n')
            f.writelines([x + '\n' for x in value])
    print(f"\nall idioms have been output to '{txt_path}'.\n")


if __name__ == '__main__':
    main()
