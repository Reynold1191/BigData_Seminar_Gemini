import pandas as pd
import facebook_scraper as fs

def get_post_id(url):
    start = url.find("pfbid")
    end = url.find("?", start)

    # Extract the part of the URL
    if start != -1 and end != -1:
        extracted_id = url[start:end]
    else:
      extracted_id = url[start:] if start != -1 else None

    return extracted_id

def scrape_comments(post_id, max_comments):
    max_comments = 20

    gen = fs.get_posts(
        post_urls=[post_id],
        options={"comments": max_comments, "allow_extra_requests": False}
    )

    # take 1st element of the generator which is the post we requested
    post = next(gen)

    # extract the comments part
    comments = post['comments_full']

        
    df = pd.DataFrame(comments)
    # df.drop(columns=['replies'], inplace=True)

    return df
