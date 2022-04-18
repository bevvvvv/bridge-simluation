"""Minmax search
"""
from venv import create
from treelib import Node, Tree


def decide(tree: Tree):
    return tree

def create_tree() -> Tree:
    tree = Tree()
    # store trick state in data
    tree.create_node("Root", "root", data={})
    tree.create_node("One", "one", parent="root")
    tree.create_node("Two", "two", parent="root")
    return tree

if __name__ == "__main__":
    print(decide(create_tree()))