class Address:
    def __init__(self, add_hash):
        self.add_hash = add_hash
        self.spending_transactions = []
        self.earning_transactions = []
        self.coins_connected = []

    