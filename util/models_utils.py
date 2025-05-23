import joblib
import re

def load_models():
    mis_model = joblib.load("model/misinformation_model.pkl")
    mis_vectorizer = joblib.load("model/misinformation_vectorizer.pkl")
    sar_model = joblib.load("model/sarcasm_model.pkl")
    sar_vectorizer = joblib.load("model/sarcasm_vectorizer.pkl")
    return mis_model, mis_vectorizer, sar_model, sar_vectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict_text(text, mis_model, mis_vectorizer, sar_model, sar_vectorizer):
    clean = clean_text(text)
    mis_vec = mis_vectorizer.transform([clean])
    sar_vec = sar_vectorizer.transform([clean])
    mis_pred = mis_model.predict(mis_vec)[0]
    sar_pred = sar_model.predict(sar_vec)[0]
    return mis_pred, sar_pred

def predict_file(file_path, mis_model, mis_vectorizer, sar_model, sar_vectorizer):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        return predict_text(file_content, mis_model, mis_vectorizer, sar_model, sar_vectorizer)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred while reading or processing the file: {e}")
        return None, None 
