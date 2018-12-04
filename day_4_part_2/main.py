import re
from datetime import datetime

import numpy as np
import pandas as pd

if __name__ == '__main__':
    messages = []
    with open('../day_4_part_1/input.txt', encoding='utf-8') as lines:
        for line in lines:
            m = re.match('\[(.*)\] (.*)', line)
            date, message = m.groups()
            date = datetime.strptime(date, '%Y-%m-%d %H:%M')
            messages.append((date, message))

    messages.sort(key=lambda x: x[0])

    # building records
    records = []
    curr_guard = None
    for date, message in messages:
        if message == 'falls asleep':
            pass
        elif message == 'wakes up':
            pass
        else:
            m = re.match('Guard #(\d+) begins shift', message)
            curr_guard = m.group(1)
            message = 'begins shift'
        record = {'guard': curr_guard, 'message': message, 'date': date}
        records.append(record)

    # preparing data for dataframe
    day_records = []
    curr_day = np.zeros(60, dtype=np.int32)
    sleep_start = None
    curr_date = None
    minute_columns = []
    for i in range(len(curr_day)):
        minute_columns.append(i)
    for record in records:
        message = record['message']
        date = record['date']
        if message == 'falls asleep':
            sleep_start = date.minute
        elif message == 'wakes up':
            curr_day[sleep_start:date.minute] = 1
            curr_date = date
        elif message == 'begins shift':
            curr_day = np.zeros(60)
            sleep_start = None
            curr_date = None
        else:
            raise RuntimeError('something fucked up')
        record = {'guard': record['guard'], 'day': curr_date}
        for col in minute_columns:
            record[col] = curr_day[col]
        day_records.append(record)

    # building dataframe and doing calculations
    df = pd.DataFrame(day_records)

    df['sleep_time'] = df[minute_columns].sum(axis=1)

    total_sleeps = df.groupby('guard')['sleep_time'].sum().sort_values(ascending=False)
    most_asleep_guard = total_sleeps.index[0]

    asleep_guard_schedule = df[df['guard'] == most_asleep_guard][minute_columns]
    most_asleep_minute = asleep_guard_schedule.sum(axis=0).sort_values(ascending=False).index[0]
    print(int(most_asleep_guard) * most_asleep_minute)
