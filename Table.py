from AVLTree import AVL
from AVLTree import AVLNode
from TableData import TableData
import copy

def height(node: AVLNode):
    if node is None:
        return -1
    else:
        return max(height(node.left), height(node.right)) + 1

class EvaluatedPath:

    def __init__(self, is_balanced, ev_path):
        self._is_balanced = is_balanced
        self._ev_path = ev_path

    def __str__(self):
        return "path: " + str(self._ev_path) + ", is_balanced: " + str(self.is_balanced())

    def is_balanced(self):
        return self._is_balanced

    def get_ev_path(self):
        return self._ev_path

    def get_path_length(self):
        return len(self._ev_path)

class Table:

    def __init__(self, tree: AVL):
        self._tree = copy.deepcopy(tree)
        self._external_nodes = self._tree.get_external_nodes()
        self._data = TableData()
        self._new_child_nodes = self._edit_tree_to_contain_new_nodes()
        print(self._tree)
        node_paths = map(lambda node: self._get_path_to_unbalanced_or_root_from_external(node), self._new_child_nodes)
        print(list(map(str, map(lambda x: x.parent.key, self._new_child_nodes))))
        self._tree = tree
        for node_path in node_paths:
            print(list(map(str, map(lambda x: x.key, node_path + [node_path[-1].parent]))))
            ev_path = self._evaluate_path(node_path)
            print(ev_path)
            self._retrieve_data_from_evaluated_path(ev_path)

    def _edit_tree_to_contain_new_nodes(self) -> [AVLNode]:
        new_child_nodes = []
        for node in self._external_nodes:
            if node.left is None:
                node.left = AVLNode(node, -1)
                new_child_nodes.append(node.left)
            if node.right is None:
                node.right = AVLNode(node, -1)
                new_child_nodes.append(node.right)
        return new_child_nodes

    def _get_path_to_unbalanced_or_root_from_external(self, node: AVLNode) -> [AVLNode]:
        """Retrieve path which leads from :param node to closest unbalanced node. If no such exists, retrieve path to
        root"""
        path = []
        current = node
        while current.is_balanced() and current is not self._tree.root:
            path.append(current)
            current = current.parent
        return path

    def _evaluate_path(self, path: [AVLNode]) -> EvaluatedPath:
        """Evaluate path - assign +/- and determine, whether subtree remains balanced when external node is added"""
        is_balanced = True
        ev_path = []
        for node in path:
            if node.is_left_child():
                ev_path.append('-')
            else:
                ev_path.append('+')
        is_left_subtree = ev_path[-1] == '-'
        is_right_subtree = not is_left_subtree
        current_root = path[-1].parent
        if (is_left_subtree and height(current_root.left) - (height(current_root.right) - 1) >= 2) or\
           (is_right_subtree and height(current_root.right) - (height(current_root.left) - 1) >= 2):
            is_balanced = False
        return EvaluatedPath(ev_path = ev_path, is_balanced = is_balanced)

    def _retrieve_data_from_evaluated_path(self, ev_path: EvaluatedPath) -> None:
        if ev_path.is_balanced():
            self._data.new_no_rotation_event(ev_path.get_path_length())
        else:
            last_two = ev_path.get_ev_path()[-2:]
            if '-' in last_two and '+' in last_two:
                self._data.new_double_rotation_event(ev_path.get_path_length())
            else:
                self._data.new_single_rotation_event(ev_path.get_path_length())

    def print_table(self) -> None:
        template = "{:^15} | {:^03.3f} | {:^03.3f} | {:^03.3f}"
        threshold = 5
        divisor = len(self._new_child_nodes)
        print(len(self._new_child_nodes))
        print("{:^15} | {:^5} | {:^5} | {:^5}".format("path length", "N_R", "S_R", "D_R"))
        print("---------------------------------------")
        for i in range(1, threshold + 1):
            print(template.format(str(i), self._data.get_no_rotation_events(i) / divisor,
                                      self._data.get_single_rotation_events(i) / divisor,
                                      self._data.get_double_rotation_events(i) / divisor))
        print(template.format(">" + str(threshold), self._data.get_accumulated_no_rotations_above_threshold(threshold) / divisor,
                              self._data.get_accumulated_single_rotations_above_threshold(threshold) / divisor,
                              self._data.get_accumulated_double_rotations_above_threshold(threshold) / divisor))