from models.lda_model import LDAModel
from models.svd_model import SVDModel
from models.tfidf_model import TFIDFModel


def train_models():
    print('Starting pre-training models...')
    lda_model = LDAModel()
    lda, corpus_tf_idf, df_docs_topics = lda_model.train_model()  # train a LDA model
    lda_model.save_model(lda, corpus_tf_idf, df_docs_topics)  # save model for recommendations use
    svd_model = SVDModel()
    data, movies, users = svd_model.load_data()
    U, sigma, Vt, predicted_ratings = svd_model.train(data, 20)
    svd_model.save(U, sigma, Vt, predicted_ratings, movies, users)
    '''
    tfidf_model = TFIDFModel()
    indices, similarities = tfidf_model.train()
    tfidf_model.save(indices, similarities)
    '''
    print('Finished pre-training models...')
