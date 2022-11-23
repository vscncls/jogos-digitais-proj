class CoinsCount:
    def __init__(self) -> None:
        self.count = 0

    def add(self):
        self.count += 1

    def amount(self):
        return self.count
