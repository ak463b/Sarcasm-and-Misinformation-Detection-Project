import pandas as pd
from datetime import datetime
import os

def save_feedback(name, comment):
    data = {"name": name, "comment": comment, "timestamp": datetime.now()}
    df = pd.DataFrame([data])
    if os.path.exists("feedback_data.csv"):
        df.to_csv("feedback_data.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("feedback_data.csv", index=False)