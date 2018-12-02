import time
import pandas as pd
import pickle
from flask_restful import fields, marshal

from models.user_rating import UserRatingModel

fields = {
    'id': fields.Integer,
    'userId': fields.Integer,
    'movieId': fields.Integer,
    'rating': fields.Float,
    'createdAt': fields.DateTime
}


class SVDRecommender:
    def __init__(self):
        self.U = SVDRecommender.load_pickle_file('./models/SVD/u')
        self.sigma = SVDRecommender.load_pickle_file('./models/SVD/sigma')
        self.Vt = SVDRecommender.load_pickle_file('./models/SVD/vt')
        self.predicted_ratings = SVDRecommender.load_pickle_file('./models/SVD/predicted_ratings')

    @staticmethod
    def load_pickle_file(file_name):
        file = open(f'{file_name}.pickle', 'rb')
        object_file = pickle.load(file)
        return object_file

    def recommend(self, user_id, n=10):
        start = time.time()

        ratings_df = self.predicted_ratings
        user_rated_movies = pd.DataFrame(marshal(UserRatingModel.query.filter_by(userId=user_id).all(), fields))['movieId'].values
        predicted_ratings = pd.DataFrame(ratings_df.loc[user_id])
        predicted_ratings.columns = ['rating']
        recommended_movies = predicted_ratings.drop(user_rated_movies).sort_values(['rating'], ascending=False).head(n)

        end = time.time()
        print(f'Finished in: {end - start}')

        # return recommended movies
        recommendations = [{'id': index, 'rating': float(row.rating)} for index, row in recommended_movies.iterrows()]
        num_of_rated_items = len(user_rated_movies)
        return num_of_rated_items, recommendations
