import jieba
import jieba.analyse
import csv
import traceback

post_index = 1
comment_index = 10
reply_index = 18
jieba.load_userdict('dict.txt.big')

try:
    file = open('2023-06-25_Gooaye_data.csv', 'r')
    reader = csv.reader(file)
    next(reader)
    text_dict = {}
    sentiments_dict = {}
    for row in reader:
        if row[post_index] != '':
            tags = jieba.analyse.extract_tags(row[post_index], topK=5)
            print(tags)

    file.close()
except Exception as e:
    file.close()
    traceback.print_exc()