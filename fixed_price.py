import csv
import ast

filename = "parsed_with_tagging.csv"
def main():
    f = open(filename, "r")
    reader = csv.reader(f, delimiter=',', quotechar='\"')

    piid_dict = {}
    for row in reader:
        piid_entry = row[2]
        print(ast.literal_eval(piid_entry))

    f.close()

if __name__ == "__main__":
    main()
