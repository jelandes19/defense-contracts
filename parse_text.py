import re
import csv
from tagger import tagged_dollars
input_file_name = "step03_contract_original.txt"
ls = None

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
            
percent_regex = "([0-9]+(.[0-9]+)? *((\%)|(percent)))"
r = re.compile(percent_regex)
def find_percent(string):
    return [x[0] for x in list(r.findall(string))]

def main():
    global ls
    ls = lines(input_file_name)
    ls = by_url(ls)

    """
    d = f()
    handle = open("fixed.csv","w")
    for v in d:
        handle.write(str(v) + ", "  + str(d[v]) + '\n')
    handle.close()
    """

    f = open("parsed.csv", "w", newline='')
    writer = csv.writer(f, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
    for url in ls:
        for i in range(len(ls[url])):
            s = ls[url][i]
            print(str((url, i)))
            dollars = tagged_dollars(s)
            if len(dollars) == 1:
                writer.writerow([str(url), str(i + 1), str(find_piids(s)),
                                 str(dollars[0][0]), str(dollars[0][1])])
            elif len(dollars) > 1:
                writer.writerow([str(url), str(i + 1), str(find_piids(s)),
                                 str(dollars[0][0]), str(dollars[0][1])])
                for d in dollars[1:]:
                    writer.writerow(["", "", "", str(d[0]), str(d[1])])

def f():
    global ls
    piid_dict = {}
    for url in ls:
        for i in range(len(ls[url])):
            s = ls[url][i]
            piids = find_piids(s)
            if(len(piids) == 1):
                if piids[0] not in piid_dict:
                    piid_dict[piids[0]] = tagged_dollars(s)
                else:
                    piid_dict[piids[0]] += tagged_dollars(s)

    for v in piid_dict:
        filtered = []
        for x in piid_dict[v]:
            if 'fixed-price' in x[1] or 'fixed price' in x[1] or 'firm-fixed-price' in x[1] or 'firm fixed-price' in x[1] or 'firm fixed price' in x[1]:
                filtered.append(process(x[0]))
        piid_dict[v] = sum(filtered)

    filtered = {}
    for v in piid_dict:
        if piid_dict[v] != 0:
            filtered[v] = piid_dict[v]
    return filtered

def process(dollar):
    if 'million' in dollar:
        return process(dollar[:len(dollar) - len('million')].strip()) * 1000000
    if 'billion' in dollar:
        return process(dollar[:len(dollar) - len('million')].strip()) * 1000000000
    dollar = dollar.replace(',', '')
    dollar = dollar.replace('$', '')
    return float(dollar)

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

def find_soft_dollar(string):
    return soft_dollar_regex.findall(string)

def find_point_dollar(string):
    return point_dollar_regex.findall(string)

def find_piids(string):
    return piid_regex.findall(string)

def find_dollar_indices(string):
    dollars = dollar.reg

def find_dollars(string):
    dollars = dollar_regex.findall(string)

    # Clean the result
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

    return dollars

def find_url(lines, url):
    return [x for x in lines if x.split()[0] == str(url)]

if __name__ == "__main__":
   main()
