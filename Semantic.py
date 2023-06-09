import jieba
import jieba.analyse
import csv
import traceback
from pprint import pprint
from snownlp import SnowNLP

# 設定 CSV 內，貼文、回應與回覆的欄位索引
post_index = 1
comment_index = 10
reply_index = 18

# 載入 jieba 套件的文字解析基本資料檔
jieba.load_userdict('dict.txt.big')

# 載入贅字資料
def get_trash_text():
    return ['\n', '/', ' ', '🏻', 'https', 'http', 'www', 'com', '👇',
    '的', '了', '在', '是', '我', '有', '和', '就', 
    '不', '人', '都', '一', '一個', '上', '也', '大', 
    '到', '為', '們', '你', '會', '而', '著', '他', '這', 
    '中', '可以', '她', '其', '對', '有些', '這個', '那個', '像', 
    '這種', '那種', '如此', '那樣', '如同', '之類', '總是', '只是', '只有',
    '便', '然後', '仍然', '卻', '如果', '只是', '只', '僅僅', '甚至', '竟然', 
    '居然', '的話', '反而', '卻', '似乎', '貌似', '大概', '恰恰', '簡直', '只不過', 
    '總', '究竟', '難道', '但是', '然而', '偏偏', '無論', '無非', '例如', '那麼',
    '要是', '果然', '似的', '越', '比如', '可能', '一定', '並且', '而且', '畢竟',
    '應該', '必須', '絕對', '特別', '尤其', '無比', '極其', '特殊', '尤為', '尤其',
    '實在', '真的', '真正', '完全', '確實', '事實上', '實際上', '根本', '其實', '簡單', 
    '簡易', '真', '絕對', '實質', '基本', '全部', '總共', '全', '全都', '全然', 
    '完完全全', '始終', '終於', '一直', '總是', '有些', '一些', '幾乎', '大約', '差不多', 
    '大部分', '許多', '好多', '多', '很多', '大家', '所有', '凡是', '一切', '什麼', 
    '哪兒', '哪裡', '哪', '怎麼', '怎樣', '如何', '何等', '何其', '多麼', '那麼', 
    '多少', '那些', '這些', '各種', '各樣', '許多', '所有', '總的來說', '總的來看', 
    '總的說來', '總的而言', '總體來看', '大體上', '基本上', '一般', '通常', '常常', '經常', 
    '或許', '也許', '可能', '或者', '也好', '也罷', '即使', '就算', '縱然', '儘管', 
    '及時', '即便', '雖然', '儘管', '儘管如此', '然而', '但是', '可是', '不過', '除非', 
    '只要', '除非', '至於', '關於', '至於', '以至於', '只不過', '只', '僅僅', '而已',
    '的話', '之', '和', '及', '與', '且', '或', '但', '然', '雖', '的', '地', '得', '而', '吧', '啊', '沒', '要', '啦', '很', '就是', '被', '才', '嗎', '這麼', '好', '放',
    '。', '，', '！', '？', '「', '」', '『', '』', '：', '；', '、', '（', '）', '【', '】', '《', '》', '〈', '〉', '＊', '……', '—', '～', '“', '”', '‘', '’', '〔', '〕', '［', '］',
    '.', ',', '!', '?', '<', '>', '/', '\\', '|', '[', ']', '{', '}', '+', '=', '-', '_', '*', '&', '^', '%', '$', '#', '@', '~', '`', '(', ')', ':', ';', ' ']

try:
    # 開啟檔案並使用讀取模式
    file = open('2023-06-25_Gooaye_data.csv', 'r')
    reader = csv.reader(file)

    # 跳過第一列，因為是標題
    next(reader)

    # 設定 dictionary 來儲存斷詞、情緒與每篇文章的情緒分數
    text_dict = {}
    sentiments_dict = {}
    sentiments_for_post = {}
    trash_text = get_trash_text()
    for row in reader:
        # 如果讀到的列是貼文資料，則顯示相關 Tag，並設定 sentiments_for_post 的初始資料結構
        if row[post_index] != '':
            tags = jieba.analyse.extract_tags(row[post_index], topK=5)
            post_text = row[post_index]
            sentiments_for_post[post_text] = []
            print(tags)

        # 如果讀到的列是貼文資料，因為後面回應與回覆部分是空白的，可以直接跳過
        if len(row) < 11:
            continue

        # 如果讀到的列是回應資料，則分析解構回應內容，並儲存進 text_dict 中
        if row[comment_index] != '':
            seg_list = jieba.cut(row[comment_index]) 
            for seg in seg_list:
                if seg in trash_text:
                    continue

                if seg in text_dict:
                    text_dict[seg] += 1
                else: 
                    text_dict[seg] = 1
            
            # 分析回應的情緒分數，並儲存進 sentiments_dict 與 sentiments_for_post
            s = SnowNLP(row[comment_index])
            sentiments_dict[row[comment_index]] = s.sentiments
            sentiments_for_post[post_text].append(s.sentiments)

        # 如果讀到的列是回應資料，因為後面回覆部分是空白的，可以直接跳過
        if len(row) < 19:
            continue

        # 如果讀到的列是回覆資料，則分析解構回覆內容，並儲存進 text_dict 中
        if row[reply_index] != '':
            seg_list = jieba.cut(row[reply_index]) 
            for seg in seg_list:
                if seg in trash_text:
                    continue

                if seg in text_dict:
                    text_dict[seg] += 1
                else: 
                    text_dict[seg] = 1

            # 分析回覆的情緒分數，並儲存進 sentiments_dict 與 sentiments_for_post
            s = SnowNLP(row[reply_index])
            sentiments_dict[row[reply_index]] = s.sentiments
            sentiments_for_post[post_text].append(s.sentiments)

    # 印出斷詞結果
    seg_data = sorted(text_dict.items(), key=lambda d:d[1], reverse=True)
    print(seg_data)

    # 印出每個回應與回覆的情緒分數
    sentiments_data = sorted(sentiments_dict.items(), key=lambda d:d[1], reverse=True)
    pprint(sentiments_data)

    # 印出每篇文章的平均情緒分數
    for post, sentiment in sentiments_for_post.items():
        sentiments_for_post[post] = sum(sentiment) / len(sentiment)
    sentiments_for_post_data = sorted(sentiments_for_post.items(), key=lambda d:d[1], reverse=True)
    pprint(sentiments_for_post_data)

    file.close()
except Exception as e:
    file.close()
    traceback.print_exc()