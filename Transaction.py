
class Transaction:
    def __init__(self, hash, timestamp):
        self.hash = hash
        self.timestamp = timestamp
        self.inputs = []
        self.outputs = []

