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

        if len(row) < 11:
            continue

        if row[comment_index] != '':
            seg_list = jieba.cut(row[comment_index]) 
            for seg in seg_list:

                if seg in text_dict:
                    text_dict[seg] += 1
                else: 
                    text_dict[seg] = 1

        if len(row) < 19:
            continue
        if row[reply_index] != '':
            seg_list = jieba.cut(row[reply_index]) 
            for seg in seg_list:
                if seg in text_dict:
                    text_dict[seg] += 1
                else: 
                    text_dict[seg] = 1

    seg_data = sorted(text_dict.items(), key=lambda d:d[1], reverse=True)
    print(seg_data)

    file.close()
except Exception as e:
    file.close()
    traceback.print_exc()