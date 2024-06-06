#facility_guide.py
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.is_available = True

    def add_child(self, child_node):
        self.children.append(child_node)

    def set_availability(self, is_available):
        self.is_available = is_available
        for child in self.children:
            child.set_availability(is_available)

class Tree:
    def __init__(self, root_name):
        self.root = TreeNode(root_name)

    def add_node(self, parent_name, child_name):
        parent_node = self.find(self.root, parent_name)
        if parent_node:
            parent_node.add_child(TreeNode(child_name))
        else:
            print(f"Parent node '{parent_name}' not found.")

    def find(self, node, name):
        if node.name == name:
            return node
        for child in node.children:
            found_node = self.find(child, name)
            if found_node:
                return found_node
        return None

    def set_node_availability(self, node_name, is_available):
        node = self.find(self.root, node_name)
        if node:
            node.set_availability(is_available)
        else:
            print(f"Node '{node_name}' not found.")
