# -*- coding: utf-8 -*-

import os


def main():
    # 所有停用词表文件所在的文件夹
    dir_path = r"./stopwords"
    save_path = r"./stopwords.txt"
    # 停用词文件编码
    file_encoding = "utf-8"
    # 合并停用词表
    all_words = set()
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        print(f"开始合并'{file}'中的停用词")
        with open(file_path, "r", encoding=file_encoding) as f:
            words = f.read().split("\n")
            words = [word for word in words if len(word) > 0]
            all_words = all_words | set(words)
    all_words = list(all_words)
    all_words.sort()
    stopwords = "\n".join(all_words)
    with open(save_path, "w", encoding=file_encoding) as f:
        f.write(stopwords)
    print(f"停用词合并完成，已保存至'{save_path}'")


if __name__ == '__main__':
    main()
