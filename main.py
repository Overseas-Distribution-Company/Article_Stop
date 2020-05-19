import data_retriever
import article

if __name__ == '__main__':

    article = data_retriever.load_article_transactions('B00036')
    article.calculate_weights()
    article.create_weight_plot()
