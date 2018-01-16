from AVLTree import *
from Table import Table
import random

avl_tree = AVL()

numbers = list(range(100, 2001))
random.shuffle(numbers)
numbers = numbers[:1000]
for n in numbers:
    avl_tree.insert(n)

print(avl_tree)

table = Table(avl_tree)
table.print_table()
