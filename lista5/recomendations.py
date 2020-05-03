from copy import deepcopy

import pandas as pd
import numpy as np


def test_ratings():
    ratings = np.zeros((9019, 1))
    ratings[2571] = 5
    ratings[32] = 4
    ratings[260] = 5
    ratings[1097] = 4

    return ratings


def get_movies_and_ratings():
    MAX = 10000
    df_r = pd.read_csv("ml-latest-small/ratings.csv")
    df_m = pd.read_csv("ml-latest-small/movies.csv")

    movies = df_m.loc[df_m.movieId < MAX, ["movieId", "title"]].to_numpy()
    ratings_data = df_r.loc[
        df_r.movieId < MAX, ["userId", "movieId", "rating"]
    ].to_numpy()

    ratings = np.zeros((611, 9019))
    for data in ratings_data:
        ratings[int(data[0]), int(data[1])] = data[2]

    return movies, ratings


def get_recommended_movies(movies, ratings, user_ratings, count=10):
    x = deepcopy(ratings)
    y = deepcopy(user_ratings)

    y = np.nan_to_num(y / np.linalg.norm(y))
    X = np.nan_to_num(x / np.linalg.norm(x, axis=0))

    z = np.dot(X, y)
    Z = np.nan_to_num(z / np.linalg.norm(z))
    recommendations = np.dot(X.T, Z)

    recommended_movies = [
        (recommendations[movie[0]][0], movie[1]) for movie in movies
    ]

    return sorted(recommended_movies, key=lambda e: e[0], reverse=True)[:count]


def main():
    movies, ratings = get_movies_and_ratings()

    user_profile = test_ratings()
    count = 10
    recommendations = get_recommended_movies(
        movies, ratings, user_profile, count
    )

    print(f"Top {count} recommendations.")
    print("Score\t\t\tTitle")
    for score, movie in recommendations:
        print(f"{score}\t{movie}")


if __name__ == "__main__":
    main()
