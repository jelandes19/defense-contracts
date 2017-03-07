import os, sys

directory = "piid_csvs"

def main():
    names = os.listdir(directory)
    outfile_name = "combined_piid_data.csv"
    outfile = open(outfile_name, "w")
    for name in names:
        f = open(directory + "/" + name, "r")
        print("Writing " + name)
        for line in f.read().splitlines()[1:]:
            outfile.write(line + "\n")

if __name__ == "__main__":
    main()
