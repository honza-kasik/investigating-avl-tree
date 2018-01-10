from AVLTree import *
import random
from collections import defaultdict

avl_tree = AVL()

numbers = list(range(100, 2001))
random.shuffle(numbers)
numbers = numbers[:100]
for n in numbers:
    avl_tree.insert(n)

print(avl_tree)
print(list(map(str, avl_tree.get_external_nodes())))

rotation_not_needed = defaultdict(lambda: 0, key="some_value")
double_rotation_needed = defaultdict(lambda: 0, key="some_value")
single_rotation_needed = defaultdict(lambda: 0, key="some_value")

max_path_length = 0

external_nodes = avl_tree.get_external_nodes()
for node in external_nodes:
    current = node
    walk = []
    is_rotation_needed = False
    # imaginary additional node
    if not current.is_leaf() and current.left is None:
        walk.append(0)
    else:
        walk.append(1)
    while current.is_balanced() and current is not avl_tree.root:
        if current.is_right_child():
            walk.append(1)
        elif current.is_left_child():
            walk.append(0)
        current = current.parent

    height_left = height(current.left)
    height_right = height(current.right)
    print(walk)
    print(str(current.key))
    last_turn = walk[-1]
    if (current.get_balance_factor() < 0 and last_turn == 0) or (current.get_balance_factor() > 0 and last_turn == 1):
        is_rotation_needed = True

    path_length = len(walk)

    if is_rotation_needed:
        last_two_turns = walk[-2:]
        if last_two_turns == [0, 1] or last_two_turns == [1, 0]:
            double_rotation_needed[path_length] += 1
        else:
            single_rotation_needed[path_length] += 1
    else:
        rotation_not_needed[path_length] += 1

    if path_length > max_path_length:
        max_path_length = path_length

print("{:^15} | {:^5} | {:^5} | {:^5}".format("path length", "N_R", "S_R", "D_R"))
print("---------------------------------------")
for i in range(1, min(max_path_length, 5) + 1):
    n_rot = rotation_not_needed[i] / len(external_nodes)
    s_rot = single_rotation_needed[i] / len(external_nodes)
    d_rot = double_rotation_needed[i] / len(external_nodes)
    print("{:^15} | {:^03.3f} | {:^03.3f} | {:^03.3f}".format(i, n_rot, s_rot, d_rot))

d_rot_rest = 0
s_rot_rest = 0
n_rot_rest = 0
for i in range(min(max_path_length, 5), max_path_length + 1):
    d_rot_rest += double_rotation_needed[i]
    s_rot_rest += single_rotation_needed[i]
    n_rot_rest += rotation_not_needed[i]
print("{:^15} | {:^03.3f} | {:^03.3f} | {:^03.3f}".format(">5", n_rot_rest / len(external_nodes),
                                                          s_rot_rest / len(external_nodes),
                                                          d_rot_rest / len(external_nodes)))