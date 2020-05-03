from __future__ import annotations

import random
from typing import Any, List


class Node:
    def __init__(self, data: Any = None):
        self.data = data
        self._children: List[Node] = []
        self.height = 0

    def __iter__(self):
        return iter(self._children)

    def __len__(self):
        return len(self._children)

    def __str__(self):
        def to_list(node: Node):
            if len(node) == 0:
                return [node.data]
            return [node.data] + [to_list(child) for child in node]

        return str(to_list(self))

    def add(self, child: Node):
        self._children.append(child)
        self.height = max(child.height for child in self._children) + 1

    def extend(self, children: List[Node]):
        self._children.extend(children)
        self.height = max(child.height for child in self._children) + 1

    @staticmethod
    def random_tree(height, children_max=5, children_min=0):
        assert children_max - children_min > 1

        def tree_factory(max_height: int, match_max=True):
            node = Node(0)

            if max_height == 0:
                return node

            gen_children_prob = (
                [
                    random.random()
                    for _ in range(
                        random.randrange(children_min, children_max)
                    )
                ]
                + [1.0]
                if match_max
                else [random.random()]
            )

            random.shuffle(gen_children_prob)

            height_matched = not match_max

            for prob in gen_children_prob[:-1]:
                if prob > 0.5:
                    child = tree_factory(max_height - 1, False)
                    if child.height == max_height - 1:
                        height_matched = True
                    node.add(child)

            node.add(tree_factory(max_height - 1, not height_matched))
            node.data = node.height
            return node

        return tree_factory(height)

    def dfs(self):
        def _dfs(tree: Node):
            if tree is not None:
                yield tree.data
                for child in tree:
                    yield from _dfs(child)

        yield from _dfs(self)

    def bfs(self):
        queue = [self]
        while len(queue) > 0:
            node = queue.pop(0)

            yield node.data

            for child in node.children:
                if child is not None:
                    queue.append(child)


def main():
    tree = Node.random_tree(5)

    print(tree)


if __name__ == "__main__":
    main()
