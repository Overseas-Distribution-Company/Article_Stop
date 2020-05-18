import pyodbc

from article import Article
from customer import Customer

CONNECTION = pyodbc.connect(f"DRIVER=SQL Server;SERVER=10.0.0.30;"
                            f";DATABASE=Overseas_Live; UID=sa; PWD=SQLsrv4fr")


def get_article_name(article_no):
    cursor = CONNECTION.cursor()
    cursor.execute(f"""
                    SELECT TOP 1 No_ No, Description
                    FROM [ODC$Item]
                    
                    WHERE No_ = '{article_no}'
                    """)

    return cursor.fetchall()[0].Description


def load_article_transactions(article_no) -> Article:
    article = Article(article_no, get_article_name((article_no)))
    cursor = CONNECTION.cursor()
    cursor.execute(
        f'''
        SELECT [Shipment Date]   Date,
               [Qty_ (Base)]     Quantity,
               [Destination No_] customer_no,
               cu.Name           customer_name
        FROM [ODC$Posted Whse_ Shipment Line] psl

        INNER JOIN [ODC$Customer] cu
            ON cu.[No_] = psl.[Destination No_]
        WHERE [Item No_] = '{article_no}'
        ORDER BY [Shipment Date]
        '''
    )

    for row in cursor:
        if article.customer_exists(row.customer_no):
            customer = article.get_customer(row.customer_no)
        else:
            customer = Customer(row.customer_no, row.customer_name)
            article.add_customer(customer)

        customer.add_transaction(row.Date, row.Quantity)

    return article


article = load_article_transactions('S00225')
article.calculate_weights()
