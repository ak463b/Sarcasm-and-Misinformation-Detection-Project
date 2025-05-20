import praw

def fetch_reddit_posts(query, limit=5):
    reddit = praw.Reddit(
        client_id="r5EdQgtZdxfVA_F3A6FwpA",
        client_secret="9PQAvhSj06hv6JL1agllqMqJ1Uxx6g",
        user_agent="Streamlit App"
    )
    posts = reddit.subreddit("all").search(query, limit=limit)
    return [{"title": post.title} for post in posts]