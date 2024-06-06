class Node:
    def __init__(self, time, name=""):
        self.time = time
        self.name = name
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self):
        self.head = Node(None)  # Header node
        self.tail = Node(None)  # Trailer node
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def insert_between(self, time, name, predecessor, successor):
        new_node = Node(time, name)
        new_node.prev = predecessor
        new_node.next = successor
        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1
        return new_node

    def insert_at_position(self, position, time, name=""):
        current = self.head.next
        index = 1
        while current != self.tail and index < position:
            current = current.next
            index += 1
        self.insert_between(time, name, current.prev, current)

    def find(self, time):
        current = self.head.next
        while current != self.tail:
            if current.time == time:
                return current
            current = current.next
        return None

    def update(self, time, name):
        node = self.find(time)
        if node:
            node.name = name

    def delete(self, node):
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1

    def first(self):
        return self.head.next if self.head.next != self.tail else None

    def last(self):
        return self.tail.prev if self.tail.prev != self.head else None

    def delete_at_position(self, position):
        current = self.head.next
        index = 1
        while current != self.tail and index < position:
            current = current.next
            index += 1
        if current != self.tail:
            self.delete(current)

    def replace_at_position(self, position, time, name=""):
        current = self.head.next
        index = 1
        while current != self.tail and index < position:
            current = current.next
            index += 1
        if current != self.tail:
            current.time = time
            current.name = name

    def __iter__(self):
        current = self.head.next
        while current != self.tail:
            yield current
            current = current.next