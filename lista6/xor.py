import numpy as np

from neural_network import NeuralNetwork, sigmoid, relu

logic_functions = {
    "XOR": np.array([[0], [1], [1], [0]]),
    "AND": np.array([[0], [0], [0], [1]]),
    "OR": np.array([[0], [1], [1], [1]]),
}
X = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1],])


def test_activators(X, y, activator1, activator2, seed=None):
    network = NeuralNetwork(X, y, activator1, activator2, seed)

    network.train(10000)

    np.set_printoptions(precision=3, suppress=True)
    print(network.output)
    success = np.allclose(network.output, y, atol=0.001)
    print("SUCCESS" if success else "FAILURE")


def compare(X, y, seed):
    print("sigmoid-sigmoid")
    test_activators(X, y, sigmoid, sigmoid, seed)
    print("sigmoid-relu")
    test_activators(X, y, sigmoid, relu, seed)
    print("relu-sigmoid")
    test_activators(X, y, relu, sigmoid, seed)
    print("relu-relu")
    test_activators(X, y, relu, relu, seed)


def test() -> None:
    for name, function in logic_functions.items():
        print(name)
        compare(X, function, 17)


def main() -> None:
    print("10000 iterations of training.")
    for name, y in logic_functions.items():
        print(name)
        test_activators(X, y, sigmoid, relu)


if __name__ == "__main__":
    try:
        # test()
        main()
    except KeyboardInterrupt:
        pass

# conclusion:
# the most stable approach is sigmoid-relu
# with fixed seed and eta = 0.1
