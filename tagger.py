import re
import csv
input_file_name = "step03_contract_original.txt"
ls = None

class DollarMatch:
    def __init__(self, dollar, prefix, suffix):
        self.dollar = dollar
        self.prefix = prefix
        self.suffix = suffix

    def __str__(self):
        return "(" + repr(self.dollar) + ", " + repr(self.prefix) + ", " + repr(self.suffix) + ")"

    def __repr__(self):
        return str(self)

def intersperse(string, lst):
    tot = lst[0]
    for l in lst[1:]:
        tot += string
        tot += l
    return tot

def group(lines):
    grouped = []
    group = ""
    for line in lines:
        if line == "******************************\n":
            grouped.append(group)
            group = ""
        else:
            group += line
    return grouped

def by_url(lines):
    url_groups = {}
    for l in lines:
        url = int(l.split()[0])
        if url in url_groups.keys():
            url_groups[url].append(l)
        else:
            url_groups[url] = [l]
    return url_groups
            

def main():
    global ls
    ls = lines(input_file_name)
    ls = by_url(ls)

def lines(fname):
    handle = open(fname, "r")
    lines = handle.readlines()
    handle.close()
    return group(lines)

cap_or_num = "[A-Z0-9]"
piid_regex = re.compile("([A-Z0-9]{6}[-/]?[A-Z0-9]{2}[-/]?[A-Z0-9][-/]?[A-Z0-9]{4})")
word_regex = re.compile("\(?[a-zA-Z\-]+(,|\.)?$")
digit = "[0-9]"
one_digit = digit
two_digits = digit*2
three_digits = digit*3
prefix = "(" + one_digit + "|" + two_digits + "|" + three_digits + ")"
suffix = "," + three_digits
dollar_regex = re.compile("(\$" + prefix + "(" + suffix + ")" + "+" \
                        + "(.[0-9][0-9])?" \
                        + "(\.|,)?$)")
soft_dollar_regex = re.compile("(?:\$[0-9]+ billion)|(?:\$[0-9]+ million)")
point_dollar_regex = re.compile("(\$[0-9]+\.[0-9]+ (?:billion|million))")

"""
Dollar parsing
"""
# For $2,500 or $1,234,713,000
regular_dollar_regex    = "(\$" + prefix + "(" + suffix + ")+" + ")"

# For $2 million or $3 billion
soft_dollar_regex       = "(\$[0-9]+ ((b|B)illion|(m|M)illion))"

# For $1.12 million or $18.56 billion
point_dollar_regex      = "(\$[0-9]+\.[0-9]+ (?:(b|B)illion|(m|M)illion))"

# For $24,890.000, which should be interpreted as $24,890,000
accidental_period_regex = "(\$" + prefix + "(" + "(\.|,)" + three_digits + ")+" + ")" 

dollar_regex_str = "(" + intersperse("|", \
            [accidental_period_regex, soft_dollar_regex, \
             point_dollar_regex, regular_dollar_regex]) + ")"
dollar_regex = re.compile(dollar_regex_str)

def find_dollars(string):
    dollars = dollar_regex.finditer(string)
    matches = []

    for amount in dollars:
        start = amount.span()[0]
        end = amount.span()[1]
        
        matches.append(DollarMatch(string[start:end], string[:start], string[end:]))

    return matches

    # Clean the result
    """
    cleaned_dollars = []
    for d in dollars:
        if not isinstance(d, str):
            cleaned_dollars.append(d[0])
        else:
            cleaned_dollars.append(d)
    dollars = cleaned_dollars

    # Replace accidental periods
    replaced = []
    regular    = re.compile(regular_dollar_regex + "$")
    accidental = re.compile(accidental_period_regex + "$")
    for d in dollars:
        if accidental.match(d) and not regular.match(d):
            d = d.replace('.', ',')
        replaced.append(d)
    dollars = replaced
    """

    return dollars

keywords = ['maximum', 'minimum', 'indefinite delivery', 'indefinite quantity', 'fixed price',
            'modification', 'firm fixed price', 'multiple award',
            'cost plus award fee', 'cost plus fixed fee', 'cost plus', 'delivery order', 
            'face value increase']
rev_keywords = ['letter contract', 'firm fixed price', 'fixed price']

def gen_regex(string):
    return re.compile(string.replace(' ', '[ -]'))

def reverse_regex(string):
    return re.compile(string[::-1].replace(' ', '[ -]'))

key_regexes = [gen_regex(k) for k in keywords]
rev_key_regexes = [reverse_regex(k) for k in rev_keywords]
filler_words = ['in the amount of', 'amounting to', 'a', 'of', 'an estimated', 'face value', 'contract', ',']
filler_regexes = [gen_regex(k) for k in filler_words]
rev_filler_words = ['in the amount of', 'amounting to', 'a', 'of', 'an estimated', 'face value', ',']
rev_filler_regexes = [reverse_regex(k) for k in rev_filler_words]

def maximal_drop(string, regexes, recurse=True, filler_regexes=filler_regexes):
    matches = []
    while True:
        string = string.strip(' \n/')
        if recurse:
            string = maximal_drop(string, filler_regexes, recurse=False)[1]
        found = False
        for k in regexes:
            m = k.match(string)
            if m:
                start = m.span()[0]
                end = m.span()[1]
                matches.append(string[start:end])
                string = string[end:]
                found = True
                break
        if not found:
            return (matches, string)

def forward_drop(string):
    return maximal_drop(string, key_regexes)

def reverse_drop(string):
    (matches, string) = maximal_drop(string[::-1], rev_key_regexes, filler_regexes=rev_filler_regexes)
    return ([x[::-1] for x in matches], string[::-1])
    
def tagged_dollars(string):
    matches = find_dollars(string)
    tagged = []
    for m in matches:
        amount = m.dollar
        tags = forward_drop(m.suffix)[0]
        tags += reverse_drop(m.prefix)[0]
        tagged.append((amount, tags))
    return tagged

def find_url(lines, url):
    return [x for x in lines if x.split()[0] == str(url)]

if __name__ == "__main__":
   main()

