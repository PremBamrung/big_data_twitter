import string
import re
from itertools import groupby
from textblob import TextBlob
from datetime import datetime
import datefinder
from langdetect import detect
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords")


PUNCT_TO_REMOVE = string.punctuation


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", PUNCT_TO_REMOVE))


def remove_urls(text):
    url_pattern = re.compile(
        r"https?://\S+|www\.\S+|[\S]+\.(net|com|org|info|edu|gov|uk|de|ca|jp|fr|au|us|ru|ch|it|nel|se|no|es|mil)[\S]*\s?"
    )
    return url_pattern.sub(r"website ", text)


def remove_html(text):
    html_pattern = re.compile("<.*?>")
    return html_pattern.sub(r"", text)


def remove_extra_spaces(text):
    space_pattern = r"\s+|^\s+|\s+$"
    without_space = re.sub(pattern=space_pattern, repl=" ", string=text)
    return without_space


def remove_email(text):
    email_pattern = r"\S*@\S*\s?"
    without_email = re.sub(pattern=email_pattern, repl=" email ", string=text)
    return without_email


def remove_phone(text):
    phone_pattern = re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?", re.S)
    without_phone = re.sub(pattern=phone_pattern, repl=" phone number ", string=text)
    return without_phone


def remove_non_letters(txt):
    return re.sub("[^a-z_]", " ", txt)


def remove_number(text):
    without_number = " ".join(
        s for s in text.split() if not any(c.isdigit() for c in s)
    )
    return without_number


def remove_parenthese(text):
    return re.sub(r"\([^)]*\)", "", text)


def remove_special(text):
    # return re.sub('[@#$=+}~"()-|`_^{]', '', text)
    return text.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_’`{|}~"))


def remove_duplicated(text):
    return " ".join([k for k, v in groupby(text.split())])


def remove_stopwords(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    return " ".join(tokens_without_sw)


def clean(text):
    text = remove_urls(text)
    text = remove_email(text)
    text = remove_html(text)
    text = remove_parenthese(text)
    # text = remove_phone(text)
    text = remove_number(text)
    text = remove_special(text)
    text = remove_duplicated(text)
    text = remove_extra_spaces(text)
    text = remove_punctuation(text)
    text = remove_stopwords(text)

    return text


def get_sentiment(tweet):
    polarity = tweet.sentiment.polarity
    tweet_sentiment = ""
    if polarity > 0:
        tweet_sentiment = "positive"
    elif polarity < 0:
        tweet_sentiment = "negative"
    elif polarity == 0:
        tweet_sentiment = "neutral"
    return polarity, tweet_sentiment


def get_date(created_at, to_string=True):
    matches = datefinder.find_dates(created_at)
    if to_string:
        date = str(next(matches, None))
    else:
        date = next(matches, None)
    return date


def find_device(source):
    if "Android" in source:
        return "Android"
    elif "iPhone" in source:
        return "iPhone"
    elif "iPad" in source:
        return "iPad"
    elif "Web App" in source:
        return "Web App"
    else:
        return "Unknown"


def detect_lang(tweet):
    try:
        return detect(str(tweet))
    except:
        return "unknown"


def get_age(created_at, to_year=False):
    created = get_date(created_at, False)
    created = created.replace(tzinfo=None)
    now = datetime.now()
    age = now - created
    if to_year:
        return round(age.days / 365, 1)
    else:
        return age.days


def get_tweet(text):
    return TextBlob(text)


if __name__ == "__main__":
    text = "  On this website https://pypi.org/sponsor/. I really like,  [ ] ^ carotte banana user@xxx.com 123 any@www (740) 522-6300   78@ppp @5555 aa@111   000-000-0000  Without Mr Modi they are BIG ZEROS 45-45-145sd-  45gre6  "
    print(text)
    print("")
    print(clean(text))
