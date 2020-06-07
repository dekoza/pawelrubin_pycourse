# dodanie kolejnej warstwy polepsza wyniki

import numpy as np
import matplotlib.pyplot as plt

from neural_network import NeuralNetwork, sigmoid, tanh

tests = [
    {
        "name": "Parabola, two layers",
        "layers": [
            {"func": sigmoid, "size": 1},
            {"func": sigmoid, "size": 10},
        ],
        "x": np.linspace(-50, 50, 26),
        "test_x": np.linspace(-50, 50, 100),
        "func": lambda x: x ** 2,
        "eta": 0.5,
    },
    {
        "name": "Sine, two layers",
        "layers": [{"func": tanh, "size": 1}, {"func": tanh, "size": 10}],
        "x": np.linspace(0, 2, 21),
        "test_x": np.linspace(0, 2, 161),
        "func": lambda x: np.sin((3 * np.pi / 2) * x),
        "eta": 0.01,
    },
    {
        "name": "Parabola, three layers",
        "layers": [
            {"func": sigmoid, "size": 1},
            {"func": sigmoid, "size": 10},
            {"func": sigmoid, "size": 10},
        ],
        "x": np.linspace(-50, 50, 26),
        "test_x": np.linspace(-50, 50, 100),
        "func": lambda x: x ** 2,
        "eta": 0.1,
    },
    {
        "name": "Sine, three layers",
        "layers": [
            {"func": tanh, "size": 1},
            {"func": tanh, "size": 10},
            {"func": tanh, "size": 10},
        ],
        "x": np.linspace(0, 2, 21),
        "test_x": np.linspace(0, 2, 161),
        "func": lambda x: np.sin((3 * np.pi / 2) * x),
        "eta": 0.01,
    },
]


def mse(expected, current):
    return sum(
        [(result - current[i]) ** 2 for i, result in enumerate(expected)]
    ) / len(expected)


def plot(test):
    nn = NeuralNetwork(test["layers"], test["eta"])
    rng = test["x"] / max(test["x"])
    img = test["func"](rng)

    X = np.reshape(rng, (len(rng), 1))
    y = np.reshape(img, (len(img), 1))

    test_x = test["test_x"] / max(test["test_x"])
    test_y = test["func"](test_x)
    test_X = np.reshape(test_x, (len(test_x), 1))

    fig = plt.figure()
    original = fig.add_subplot(2, 1, 1)
    original.set_title(test["name"])
    original.scatter(rng, y)

    new = fig.add_subplot(2, 1, 2)
    new.set_title("Aproksymacja")

    for i in range(50):
        nn.train(100, X, y)
        nn.feedforward(test_X)
        new.clear()
        new.set_xlabel(f"{i*100} iteracji\nMSE: {mse(test_y, nn.output)}")
        new.scatter(test_x, nn.output)
        plt.pause(0.01)

    plt.show()


def main():
    for test in tests:
        plot(test)


if __name__ == "__main__":
    main()
