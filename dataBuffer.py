import collections


class Buffer:

    def __init__(self, header, x):
        self.buffer = {}
        for key in header:
            self.buffer.update({key: collections.deque(maxlen=x)})



    def buf(self, data):

        for key in self.buffer:
            self.buffer[key].append(data[key])

    def read_buf(self):
        return self.buffer
