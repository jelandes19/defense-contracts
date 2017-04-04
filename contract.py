class Contract:
    def __init__(self, date, url):
        self.date      = date
        self.url       = url
        self.dollars   = []

class DollarAmount:
    def __init__(self, amount):
        self.amount = amount
        self.tags = set()

    def add_tag(tag):
        tags.add(tag)

    def has_tag(tag):
        return tag in self.tags
