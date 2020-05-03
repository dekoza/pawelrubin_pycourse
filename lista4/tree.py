import random


def random_tree(height: int):
    def tree_factory(max_height: int, index=1, match_max=True):
        if max_height == 0:
            return {"tree": None, "height": 0}

        probs = (
            [1.0, random.random()]
            if match_max
            else [random.random(), random.random()]
        )
        random.shuffle(probs)

        left_subtree = (
            (tree_factory(max_height - 1, 2 * index, match_max=False))
            if probs[0] > 0.5
            else {"tree": None, "height": 0}
        )

        height_matched = left_subtree["height"] == max_height - 1

        right_subtree = (
            tree_factory(
                max_height - 1,
                2 * index + 1,
                match_max=match_max and not height_matched,
            )
            if probs[1] > 0.5 or (match_max and not height_matched)
            else {"tree": None, "height": 0}
        )

        return {
            "tree": [str(index), left_subtree["tree"], right_subtree["tree"]],
            "height": max(left_subtree["height"], right_subtree["height"]) + 1,
        }

    return tree_factory(height)


def dfs(tree):
    if tree is not None:
        yield tree[0]
        yield from dfs(tree[1])
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


def main():
    tree = random_tree(5)

    print(tree["tree"])


if __name__ == "__main__":
    main()
