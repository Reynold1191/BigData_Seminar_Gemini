import fetcher
import pandas as pd

MAX_COMMENTS = 20


def read_fb_link(link):
    post_id = fetcher.get_fb_post_id(link)
    if post_id:
        df = fetcher.scrape_fb_post_comments(post_id, MAX_COMMENTS)

        export(df, "temp_input")

        data = "\n".join(df["comment_text"])
        return data
    else:
        return None


def read_youtube_livestream_link(link):
    video_id = fetcher.get_youtube_video_id(link)
    if video_id:
        df = fetcher.get_ytb_livestream_comments(video_id, MAX_COMMENTS)

        export(df, "temp_input")

        data = "\n".join(df["comment_text"])
        return data
    else:
        return None


def read_youtube_video_link(link):
    video_id = fetcher.get_youtube_video_id(link)
    if video_id:
        df = fetcher.get_ytb_video_comments(video_id, MAX_COMMENTS)

        export(df, "temp_input")

        data = "\n".join(df["comment_text"])
        return data
    else:
        return None


def read_csv(path):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        return None

    all_comments = "\n".join(df["Comment"])
    return all_comments


def format_response(text):
    print(text)
    items = text.strip("`\n[]").split("}, {")

    comment_list = []
    for item in items:
        comment, sentiment = item.rsplit(": ", 1)
        comment_list.append(
            {
                "comment": comment.strip("{").strip("'\""),
                "sentiment": sentiment.strip("}").strip("'\""),
            }
        )

    df = pd.DataFrame(comment_list)
    export(df, "temp_output")

    return comment_list


def export(df, name):
    df.to_csv(f"data/{name}.csv", index=False, encoding="utf-8", mode="w")
