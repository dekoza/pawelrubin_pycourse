from typing import List
from pprint import pprint

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression


df = pd.read_csv("ml-latest-small/ratings.csv")
users = df.loc[df.movieId == 1, "userId"].to_numpy()


def generate_X_Y(m: int):
    Y = df.loc[
        (df.userId.isin(users)) & (df.movieId == 1), ["rating"]
    ].to_numpy()

    X_data = df.loc[
        (df.userId.isin(users)) & (df.movieId > 1) & (df.movieId <= m),
        ["userId", "movieId", "rating"],
    ].to_numpy()

    X = np.zeros((len(users), m))
    for userId, movieId, rating in X_data:
        index = np.where(users == userId)[0][0]
        X[index, int(movieId) - 2] = rating

    return X, Y


# 1a
for m in (10, 1000, 10000):
    X, Y = generate_X_Y(m)
    model = LinearRegression().fit(X, Y)

    predicted = plt.scatter(
        [i for i in range(0, 215)],
        [model.predict([X[i]]) for i in range(0, 215)],
        alpha=0.5,
    )
    actual = plt.scatter(
        [i for i in range(0, 215)],
        [Y[i] for i in range(0, 215)],
        alpha=0.5,
        c="r",
    )
    plt.legend((predicted, actual), ("Predicted", "Real"))
    plt.title(f"Predictions for {m} movies.")
    plt.show()


# 1b
TRAINING_SIZE = 200
FULL_SIZE = 215
for m in (10, 100, 200, 500, 1000, 10000):
    X, Y = generate_X_Y(m)
    t_X, t_Y = X[:TRAINING_SIZE], Y[:TRAINING_SIZE]

    model = LinearRegression().fit(t_X, t_Y)

    print(f"Prediction for {m} movies.")
    for i in range(TRAINING_SIZE, FULL_SIZE):
        print(f"{i + 1}: {model.predict([X[i]])} vs {Y[i]}")
