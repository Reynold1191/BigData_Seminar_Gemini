import scape_comments as sc
import pandas as pd

def read_fb_link(link):
    post_id = sc.get_post_id(link)
    if post_id:
        df = sc.scrape_comments(post_id, 10)
        data = '\n'.join(df['comment_text'])
        return data
    else:
        return None

def read_csv(path):
    try:
      df = pd.read_csv(path)
    except Exception as e:
      return None    

    all_comments = '\n'.join(df['Comment'])
    return all_comments

def format_response(text):
    print(text)
    items = text.strip("[]").split("}, {")

    comment_list = []
    for item in items:
        comment, sentiment = item.rsplit(": ", 1)
        comment_list.append({
            "comment": comment.strip("{"),
            "sentiment": sentiment.strip("}")
        })
    
    return comment_list