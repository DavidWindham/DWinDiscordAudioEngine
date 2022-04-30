class Queue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        # returns true if empty
        return not self.queue

    def add_to_queue(self, item_to_append) -> None:
        self.queue.append(item_to_append)

    def get_next_from_queue(self) -> dict or None:
        if not self.queue:
            return None

        # FIFO
        return self.queue.pop(0)

    def remove_item_from_queue(self, index_of_item_to_remove) -> None:
        self.queue.pop(index_of_item_to_remove)

    def empty_queue(self):
        self.queue = []

    def get_queue(self) -> list:
        return self.queue
