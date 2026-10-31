
"""Queue Object - First In, First Out (FIFO)."""

class Queue:
    def __init__(self, items=None):
        self.items = list(items or [])

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def peek(self):
        return self.items[0] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def front(self):
        return self.items[0] if self.items else None

    def rear(self):
        return self.items[-1] if self.items else None
