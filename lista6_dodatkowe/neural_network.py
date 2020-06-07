from dataclasses import dataclass
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


class NeuralNetworkLayer:
    def __init__(self, activator: Activator, shape) -> None:
        self.activator = activator
        self.weights = np.random.standard_normal(shape)
        self.values = np.zeros((shape[1]))


class NeuralNetwork:
    def __init__(self, layers, eta, output_shape=(1, 1)) -> None:
        self.layers = []
        self.output = np.zeros(output_shape)
        self.eta = eta

        for layer, next_layer in zip(layers[0:-1], layers[1:]):
            self.layers.append(
                NeuralNetworkLayer(
                    layer["func"], (next_layer["size"], layer["size"])
                )
            )

        self.layers.append(
            NeuralNetworkLayer(
                layers[-1]["func"], (output_shape[0], layers[-1]["size"])
            )
        )

    def feedforward(self, X) -> None:
        self.layers[0].values = X

        for layer, next_layer in zip(self.layers[0:-1], self.layers[1:]):
            next_layer.values = layer.activator.activation_function(
                np.dot(layer.values, layer.weights.T)
            )
        self.output = self.layers[-1].activator.activation_function(
            np.dot(self.layers[-1].values, self.layers[-1].weights.T)
        )

    def backprop(self, y) -> None:
        deltas = []

        delta = (y - self.output) * self.layers[
            -1
        ].activator.activation_derivative(self.output)
        deltas.append(self.eta * np.dot(delta.T, self.layers[-1].values))

        for layer, prev_layer in zip(
            reversed(self.layers[0:-1]), reversed(self.layers[1:])
        ):
            delta = layer.activator.activation_derivative(
                prev_layer.values
            ) * np.dot(delta, prev_layer.weights)
            deltas.append(self.eta * np.dot(delta.T, layer.values))

        for layer, weight in zip(self.layers, reversed(deltas)):
            layer.weights += weight

    def train(self, iterations: int, input_data, expected_data) -> None:
        for _ in range(iterations):
            self.feedforward(input_data)
            self.backprop(expected_data)
