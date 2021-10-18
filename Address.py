class Address:
    def __init__(self, hash):
        self.hash = hash
        self.spending_transactions = []
        self.earning_transactions = []

    