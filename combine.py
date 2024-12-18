import os, config
import pandas as pd
import spacy
import re
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import nltk

nlp = spacy.load("en_core_web_sm")
nltk.download("stopwords")

def remove_entities(text):  
    sensetive_entities = {"PERSON", "NORP", "ORG", "GPE", "LOC", "FAC"}
    
    output_words = []
    for word in nlp(text):
        if word.ent_type_ in sensetive_entities:
            output_words.append(word.ent_type_)
        else:
            output_words.append(word.text)
    
    return " ".join(output_words)

def clean_post(text):
    text = str(text)
    text = text.lower()
    text = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", " ", text)
    text = re.sub('[!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@]+', " ", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("([0-9]+)", " ", text)
    text = remove_entities(text)
    tokens = [token.lower() for token in TweetTokenizer().tokenize(text) if token.isalpha() and token not in set(stopwords.words("english"))]
    tokens = [token for token in tokens if len(token) > 1]
    return " ".join(tokens)

def get_all_csvs(folder):
    csv_files = []
    for file in os.listdir(folder):
        csv_files.append(file)
    return [f"{folder}{csv_file}" for csv_file in csv_files if csv_file.endswith(".csv")]

def main():
    csv_files = get_all_csvs(config.OUTPUT_FOLDER)
    dataframes = [pd.read_csv(file, index_col=0) for file in csv_files]
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["selftext"])
    combined_df = combined_df.reset_index(drop=True)
    combined_df["selftext"] = combined_df["selftext"].apply(clean_post)
    
    combined_df.to_csv(f"all_posts.csv", index = False)

if __name__ == "__main__":
    main()