from typing import NamedTuple
import numpy as np
import matplotlib.pyplot as plt

from neural_network import NeuralNetwork, sigmoid, relu, tanh


class TestCase(NamedTuple):
    X: np.ndarray
    y: np.ndarray
    big_x: np.ndarray


parabole = TestCase(
    X=np.linspace(-50, 50, 26),
    y=np.linspace(-50, 50, 26) ** 2,
    big_x=np.linspace(-50, 50, 101),
)

sinus = TestCase(
    X=np.linspace(0, 2, 21),
    y=np.sin((3 * np.pi / 2) * np.linspace(0, 2, 21)),
    big_x=np.linspace(0, 2, 161),
)


def main():
    for case in (parabole, sinus):
        X = case.X

        X = X / max(X)
        y = case.y

        # network accepts matrix, so we have to reshape
        X_reshaped = np.reshape(X, (len(X), 1))
        y_reshaped = np.reshape(y, (len(y), 1))

        big_x = case.big_x
        big_x = big_x / max(big_x)

        big_x_reshaped = np.reshape(big_x, (len(big_x), 1))

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_title("Original parabole")
        ax1.scatter(X, y)
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.set_title("Network generated parabole")

        network = NeuralNetwork(X_reshaped, y_reshaped, sigmoid, sigmoid,)
        for i in range(100):
            network.train(100)
            network.input = big_x_reshaped
            network.feedforward()
            ax2.clear()
            ax2.set_xlabel(f"{i * 100} iterations")
            ax2.scatter(big_x_reshaped, network.output.flatten())
            network.input = X_reshaped
            plt.pause(0.001)
        plt.show()
        # sin


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
