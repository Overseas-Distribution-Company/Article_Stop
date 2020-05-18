from datetime import date, datetime

from scipy.stats import stats

import main_weights
import pandas
import matplotlib.pyplot as plt

df = main_weights.load_item_transactions('S00225')
df2 = df.groupby('Customer')

for sub_frame in df2:
    df_frame = pandas.DataFrame(columns=['index', 'interval'])

    if len(sub_frame[1]) > 2:
        for i in range(len(sub_frame[1]) - 2):
            dys = sub_frame[1].iloc[i + 1]["Date"] - sub_frame[1].iloc[i]["Date"]
            dys = dys.days
            df_frame.loc[i] = [i, dys]

        plt.plot( df_frame['index'], df_frame['interval'])
        slope, intercept, lo_slope, up_slope = stats.theilslopes( df_frame['interval'].tolist(),df_frame['index'].tolist(), .99)
        func = lambda x : slope * x  + intercept
        func_upper = lambda x: up_slope * x + intercept
        lin_y = [func(x) for x in df_frame['index']]
        plt.plot(df_frame['index'], lin_y)
        plt.plot(df_frame['index'], [func_upper(x) for x in df_frame['index']])
        plt.plot([15],[func(15)], 'ro')
        print(sub_frame[1]["Date"][13])
        # plt.plot([15], [(datetime.today() - sub_frame[1]["Date"][13]).days], 'bo')
        print(df_frame)
        print('================================================')

    plt.show()