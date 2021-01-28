import data_retriever


if __name__ == '__main__':
    article = data_retriever.load_article_transactions('S00225')
    customer = article.get_customer('KC0450')

    article.create_weight_plot()
    customer.plot_graph()
    print(customer.transactions)
