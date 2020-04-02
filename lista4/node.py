import math
import random
from typing import List


def random_tree(height: int):
    def tree_factory(max_height: int, index=1, match_max=True):
        if max_height == 0:
            return {"tree": None}

        go_left = random.random() < 0.5
        go_right = (not go_left and match_max) or random.random() < 0.5

        left_subtree = (
            tree_factory(max_height - 1, 2 * index, match_max=False)
            if go_left
            else {"tree": None}
        )
        right_subtree = (
            tree_factory(
                max_height - 1,
                2 * index + 1,
                match_max=left_subtree["tree"] is None
                or left_subtree["height"] != max_height - 1,
            )
            if go_right
            else {"tree": None}
        )

        return {
            "tree": [str(index), left_subtree["tree"], right_subtree["tree"]],
            "height": math.floor(math.log2(index)),
        }

    return tree_factory(height)["tree"]


def dfs(tree):
    if tree is not None:
        yield from dfs(tree[1])
        yield tree[0]
        yield from dfs(tree[2])


def bfs(tree):
    queue = [tree]
    while len(queue) > 0:
        node = queue.pop(0)

        yield node[0]

        if node[1] is not None:
            queue.append(node[1])

        if node[2] is not None:
            queue.append(node[2])


class Node:
    def __init__(self, data):
        self.data = data
        self.children: List[Node] = []

    @staticmethod
    def random_tree(height):
        pass
