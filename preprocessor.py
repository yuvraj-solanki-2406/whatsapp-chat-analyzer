import re
import pandas as pd


def preprocessData(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)

    df = pd.DataFrame({"user_messages": messages, "message_date": date})
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%y, %H:%M - ")

    users = []
    messages = []

    for i in df["user_messages"]:
        pattern_1 = re.split("([\w\W]+?):\s", i)
        if pattern_1[1:]:
            users.append(pattern_1[1])
            messages.append(pattern_1[2])
        else:
            users.append("Encryption notification")
            messages.append(pattern_1[0])

    # Creating new columns --- user_name and user_message
    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_messages"], inplace=True)

    df.rename(columns={'message_date': 'date'}, inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
