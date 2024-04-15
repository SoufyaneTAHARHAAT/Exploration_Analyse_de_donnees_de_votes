import re
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

law_names = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1').filter(items = ['titre'])
law_names['titre'].unique()
law_names.dropna(subset=['titre'], inplace=True)
print(law_names)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for i in range(len(word) - 1, -1, -1): 
            char = word[i]
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search(self, word):
        current = self.root
        for i in range(len(word) - 1, -1, -1): 
            char = word[i]
            if char not in current.children:
                return False
            current = current.children[char]
        return current is not None and current.is_end_of_word
    
    def _print_tree_recursive(self, node, level):
        for char, child_node in node.children.items():
            print("  " * level + char)
            self._print_tree_recursive(child_node, level + 1)

    def print_tree(self):
        print("Root")
        self._print_tree_recursive(self.root, level=1)

tree = Trie()

for t in law_names['titre'] :
    tree.insert(t)

tree.print_tree()
