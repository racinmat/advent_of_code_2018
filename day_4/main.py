import re
from datetime import datetime
import numpy as np
import pandas as pd


def load_messages():
    messages = []
    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            date = line[1:17]
            message = line[19:].replace('\n', '')
            date = datetime.strptime(date, '%Y-%m-%d %H:%M')
            messages.append((date, message))
    messages.sort(key=lambda x: x[0])
    return messages


def build_records(messages):
    records = []
    curr_guard = None
    for date, message in messages:
        if message != 'falls asleep' and message != 'wakes up':
            m = re.match('Guard #(\d+) begins shift', message)
            curr_guard = m.group(1)
            message = 'begins shift'
        record = {'guard': curr_guard, 'message': message, 'date': date}
        records.append(record)
    return records


def build_dataframe(records):
    # preparing data for dataframe
    day_records = []
    curr_day = np.zeros(60, dtype=np.int32)
    sleep_start = None
    curr_date = None
    minute_columns = list(range(len(curr_day)))
    for record in records:
        message = record['message']
        date = record['date']
        if message == 'falls asleep':
            sleep_start = date.minute
        elif message == 'wakes up':
            curr_day[sleep_start:date.minute] = 1
            curr_date = date
        else:
            curr_day = np.zeros(60)
            sleep_start = None
            curr_date = None
        # adding multiple keys at once
        day_record = {'guard': record['guard'], 'day': curr_date, **dict(enumerate(curr_day))}
        day_records.append(day_record)
    df = pd.DataFrame(day_records)
    return df, minute_columns


def part_1():
    messages = load_messages()
    records = build_records(messages)
    df, minute_columns = build_dataframe(records)

    most_asleep_guard = df.groupby('guard')[minute_columns].sum(axis=1).sum(axis=1).idxmax()
    most_asleep_minute = df[df['guard'] == most_asleep_guard][minute_columns].sum(axis=0).idxmax()
    print(int(most_asleep_guard) * most_asleep_minute)


def part_2():
    messages = load_messages()
    records = build_records(messages)
    df, minute_columns = build_dataframe(records)

    most_asleep_guard = df.groupby('guard')[minute_columns].sum().max(axis=1).idxmax()
    most_asleep_minute = df[df['guard'] == most_asleep_guard][minute_columns].sum(axis=0).idxmax()
    print(int(most_asleep_guard) * most_asleep_minute)


if __name__ == '__main__':
    part_1()
    part_2()
