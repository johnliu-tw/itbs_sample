from facebook_scraper import get_posts
import traceback

try:
  for post in get_posts('Gooaye', pages=1, cookies='www.facebook.com_cookies.txt', extra_info=True, options={'comments': True}):
    date_string = post['time'].strftime('%Y-%m-%d %H:%M:%S')

    print(date_string)
    print(post['text'])
except Exception as e:
  traceback.print_exc()