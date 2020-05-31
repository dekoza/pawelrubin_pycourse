from typing import Callable, NamedTuple, Optional
import numpy as np


class Activator(NamedTuple):
    activation_function: Callable[[np.ndarray], np.ndarray]
    activation_derivative: Callable[[np.ndarray], np.ndarray]


sigmoid = Activator(
    lambda x: 1.0 / (1.0 + np.exp(-x)), lambda x: x * (1.0 - x)
)

relu = Activator(lambda x: x * (x > 0), lambda x: np.where(x > 0.0, 1.0, 0.0))

tanh = Activator(lambda x: np.tanh(x), lambda x: 1.0 - x ** 2)


class NeuralNetwork:
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        act1: Activator,
        act2: Activator,
        seed: Optional[int] = None,
        eta: float = 0.1,
        hidden_size: int = 4,
    ) -> None:
        self.input = x
        self.y = y
        self.output = np.zeros(self.y.shape)
        self.eta = 0.1
        self.act1, self.act1_d = act1
        self.act2, self.act2_d = act2
        self.hidden_size = hidden_size
        if seed:
            np.random.seed(seed)
        self.weights1 = np.random.rand(self.hidden_size, self.input.shape[1])
        self.weights2 = np.random.rand(1, self.hidden_size)

    def feedforward(self) -> None:
        self.layer1 = self.act1(np.dot(self.input, self.weights1.T))
        self.output = self.act2(np.dot(self.layer1, self.weights2.T))

    def backprop(self) -> None:
        delta2 = (self.y - self.output) * self.act2_d(self.output)
        d_weights2 = self.eta * np.dot(delta2.T, self.layer1)

        delta1 = self.act1_d(self.layer1) * np.dot(delta2, self.weights2)
        d_weights1 = self.eta * np.dot(delta1.T, self.input)

        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def train(self, iterations: int) -> None:
        for _ in range(iterations):
            self.feedforward()
            self.backprop()
