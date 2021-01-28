import data_retriever
import pyodbc
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def get_extract():
    wb = Workbook()
    ws = wb.create_sheet('extract')

    conn = pyodbc.connect(f"DRIVER=SQL Server;SERVER=10.0.0.30;"
                            f";DATABASE=Overseas_Live; UID=sa; PWD=SQLsrv4fr")

    cursor = conn.cursor()

    cursor.execute("""
                SELECT No_ no, Description dec
                FROM ODC$Item
                WHERE Blocked = 0
                    """)
    ws.append(['No', 'Description'])
    for row in cursor:
        article = data_retriever.load_article_transactions(row.no)
        if article.do_flag_article(0.70):
            ws.append([row.no, row.dec])
            print([row.no, row.dec])

    print('saving?')
    wb.save('extract.xlsx')


if __name__ == '__main__':
    get_extract()

