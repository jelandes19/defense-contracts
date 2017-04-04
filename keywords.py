class Keyword:
    def __init__(self, name, regex):
        self.name  = name
        self.regex = re.compile(regex)

    def name(self):
        return self.name

    def regex(self):
        return self.regex.pattern

indef_deliv = Keyword("indefinite delivery", "indefinite-?delivery")
maximum = Keyword("maximum", "maximum")
