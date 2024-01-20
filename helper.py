from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def showStats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_msgs = df.shape[0]
    words = []
    for i in df['message']:
        words.extend(i.split())

    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    extract = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_msgs, len(words), media, len(links)


def mostActiveUser(df):
    x = df['user'].value_counts().head()
    df = round(
        df['user'].value_counts() / df.shape[0] * 100, 2
        ).reset_index().rename(
         columns={'index': 'Name', 'user': 'Percentage'}
    )
    return x, df


def createWordCloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # print(df)

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    def removeStopWords(message):
        good_words = []
        for word in message.lower().split():
            if word not in stopwords:
                good_words.append(word)
        return " ".join(good_words)

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    temp['message'] = temp['message'].apply(removeStopWords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def mostCommonWords(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()
    # print(stopwords)

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    top_words = pd.DataFrame(Counter(words).most_common(20))

    return top_words


def emojiCount(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojis_df


def monthlyTimeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
