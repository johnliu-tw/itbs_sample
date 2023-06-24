from facebook_scraper import get_posts
import csv
from datetime import date
import traceback
today = date.today()
file_date = today.strftime('%Y-%m-%d')

reaction_map = {
    'like': '讚',
    'love': '大心',
    'haha': '哈',
    'sorry': '嗚',
    'wow': '哇',
    'angry': '怒',
    'care': '加油'
}
def generate_empty_list(length):
   return ['' for _ in range(length)]


csv_file = open(file_date+'_data.csv', 'a', newline='', encoding='utf_8_sig')
writer = csv.writer(csv_file)
writer.writerow(['日期', '內容', '分享數', '反應:讚', '反應:大心', '反應:哈', '反應:嗚', '反應:哇', '反應:怒', '反應:加油', 
                 '留言', '留言反應:讚', '留言反應:大心', '留言反應:哈', '留言反應:嗚', '留言反應:哇', '留言反應:怒', '留言反應:加油',
                 '留言回覆', '回覆反應:讚', '回覆反應:大心', '回覆反應:哈', '回覆反應:嗚', '回覆反應:哇', '回覆反應:怒', '回覆反應:加油'])

try:
  for post in get_posts('Gooaye', pages=1, cookies='www.facebook.com_cookies.txt', extra_info=True, options={'comments': True}):
    date_string = post['time'].strftime('%Y-%m-%d %H:%M:%S')

    print(date_string)
    print(post['text'])
    if post['reactions'] is not None:
        reaction_data = [post['reactions'].get(reaction_map['like']), 
                        post['reactions'].get(reaction_map['love']), 
                        post['reactions'].get(reaction_map['haha']), 
                        post['reactions'].get(reaction_map['sorry']), 
                        post['reactions'].get(reaction_map['wow']), 
                        post['reactions'].get(reaction_map['angry']), 
                        post['reactions'].get(reaction_map['care'])]
    else:
        reaction_data = generate_empty_list(7)
    post_data = [date_string, post['text'], post['shares']] + reaction_data
    writer.writerow(post_data)

    print('擷取回應中...')
    for comment in post['comments_full']:
        if comment['comment_reactions'] is not None:
          comment_reaction_data = [comment.get('comment_reactions').get('like'), 
                            comment.get('comment_reactions').get('love'), 
                            comment.get('comment_reactions').get('haha'), 
                            comment.get('comment_reactions').get('sorry'), 
                            comment.get('comment_reactions').get('wow'), 
                            comment.get('comment_reactions').get('angry'), 
                            comment.get('comment_reactions').get('care')]
        else:
          comment_reaction_data = generate_empty_list(7)
        comment_data = [comment['comment_text']] + comment_reaction_data
        empty_columns = generate_empty_list(len(post_data))
        writer.writerow(empty_columns + comment_data)

        for reply in comment['replies']:
            if reply['comment_reactions'] is not None:
              reply_reaction_data = [reply.get('comment_reactions').get('like'), 
                                        reply.get('comment_reactions').get('love'), 
                                        reply.get('comment_reactions').get('haha'), 
                                        reply.get('comment_reactions').get('sorry'), 
                                        reply.get('comment_reactions').get('wow'), 
                                        reply.get('comment_reactions').get('angry'), 
                                        reply.get('comment_reactions').get('care')]
            else:
              reply_reaction_data = generate_empty_list(7)
            reply_data = [reply['comment_text']] + reply_reaction_data
            empty_columns = generate_empty_list(len(post_data) + len(comment_data))
            writer.writerow(empty_columns + reply_data)
  
  csv_file.close()
except Exception as e:
  csv_file.close()
  traceback.print_exc()