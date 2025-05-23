import praw
import pandas as pd
import streamlit as st # Assuming Streamlit is used for displaying messages

def fetch_reddit_posts(query, limit=5):
    """
    Searches for posts across all subreddits based on a query and returns them as a Pandas DataFrame.
    
    Args:
        query (str): The search term for Reddit posts.
        limit (int): The maximum number of posts to fetch.

    Returns:
        pandas.DataFrame: A DataFrame containing 'title' of the fetched posts.
                          Returns an empty DataFrame if no posts are found or if there's an error.
    """
    try:
         reddit = praw.Reddit(
            client_id="Your Client_id", # Consider moving to Streamlit secrets
            client_secret="Your Client_Secret", # Consider moving to Streamlit secrets
            user_agent="Your App Name" # Consider moving to Streamlit secrets
        )
        # Search across all subreddits
        posts = reddit.subreddit("all").search(query, limit=limit)
        
        posts_data = []
        for post in posts:
            posts_data.append({
                "title": post.title,
                # You might want to add more fields like 'score', 'num_comments', 'url'
                # "score": post.score,
                # "num_comments": post.num_comments,
                # "url": post.url
            })
        
        # Return a DataFrame, even if empty
        return pd.DataFrame(posts_data)

    except Exception as e:
        st.error(f"Error fetching Reddit posts: {e}. Please check your query and API credentials.")
        return pd.DataFrame() # Return an empty DataFrame on error
