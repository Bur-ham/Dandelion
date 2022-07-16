import asyncio


class MusicQueue:
    def __init__(self, max_size = 0):
        self.max_size = max_size
        self.__items = []

    def __len__(self):
        return len(self.__items)

    def __iter__(self):
        return iter(self.__items)

    def __contains__(self, item):
        return item in self.__items

    def __getitem__(self, index):
        return self.__items[index]

    def __setitem__(self, index, value):
        self.__items[index] = value

    def __delitem__(self, index):
        del self.__items[index]

    def qsize(self):
        """
        Returns the size of the queue.
        """
        return len(self.__items)

    def empty(self):
        """
        Returns True if the queue is empty.
        """
        return len(self.__items) == 0

    def clear(self):
        """
        Clears the queue.
        """
        self.__items = []
    
    def del_track(self, start, end = None):
        """
        Deletes a track from the queue.
        """
        if end is None:
            del self.__items[start]
        else:
            del self.__items[start:end+1]

    def put(self, item):
        """
        Adds an item to the queue.
        """
        if self.qsize() == self.max_size and self.max_size > 0:
            raise asyncio.QueueFull("Queue is full")
        self.__items.append(item)

    def get(self):
        """
        Gets the next item in the queue.
        """
        return self.__items.pop(0)

    