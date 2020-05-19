import pyodbc
import pandas
import matplotlib.pyplot as plt
import numpy as np


def load_item_transactions(item_no):
    connect = pyodbc.connect(f"DRIVER=SQL Server;SERVER=10.0.0.30;"
                             f";DATABASE=Overseas_Live; UID=sa; PWD=SQLsrv4fr")

    df = pandas.read_sql_query(
        f'''
        SELECT [Shipment Date]   Date,
               [Qty_ (Base)]     Quantity,
               [Destination No_] + ' ' + cu.Name Customer
        FROM [ODC$Posted Whse_ Shipment Line] psl
        
        INNER JOIN [ODC$Customer] cu
            ON cu.[No_] = psl.[Destination No_]
        WHERE [Item No_] = '{item_no}'
        ORDER BY [Shipment Date]
        '''
        , connect)

    return df


def func(pct, allvals):
    absolute = int(pct / 100. * np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)


def generate_pie_plot(data):
    fig, ax = plt.subplots(figsize=(5, 10), subplot_kw=dict(aspect="equal"))

    wedges, texts, autotexts = ax.pie(data['Quantity'], autopct=lambda pct: func(pct, data['Quantity']),
                                      textprops=dict(color="w"))


    ax.legend(wedges, data['Customer'],
              title="Customer",
              loc="lower left",
              bbox_to_anchor=(0., 1.02, 1., .102),mode='expand')

    plt.setp(autotexts, size=8, weight="bold")

    plt.show()


if __name__ == '__main__':
    frame = load_item_transactions('S01448')
    frame = frame.groupby(['Customer'], squeeze=True, as_index=False).sum()
    sum = frame.sum()[1]
    print(sum)
    frame['Weight'] = [float(x) / sum for x in frame['Quantity']]
    generate_pie_plot(frame)
