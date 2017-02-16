from subprocess import call
from threading import Thread
import os
import sys

num_piids = 0
num_proc = 100
count = 0
default_piid_directory = "piid_csvs"
default_piid_file = "piids_trimmed.txt"
piid_directory = ""

def split(xs, n):
    xss = []
    for i in range(n):
        xss.append([])
    for i in range(len(xs)):
        j = i % n
        xss[j].append(xs[i])
    return xss

def pull(piid):
    global count
    url = "https://www.fpds.gov/ezsearch/search.do?s=FPDSNG.COM&indexName=awardfull&templateName=CSV&q=" + piid + "&renderer=jsp&length=5000"
    args = ["curl", "-L", "--silent", "--referer", "\";auto\"", "-o", os.path.join(piid_directory,str(piid) + ".txt"), url]
    call(args)
    count += 1
    print("(" + str(count) + "/" + str(num_piids) + ") piid " + piid + " done")

def pull_list(xs):
    for piid in xs:
        pull(piid)

def pull_gen(xs):
    return lambda: pull_list(xs)

def main():
    print("This program downloads csv files describing contract data from the FPDS website")
    print("Enter the file containing PIIDs of the contracts to download (<Enter> for default: ", end="")
    print(default_piid_file + ")")
    print(">>> ", end="")
    sys.stdout.flush()
    line = sys.stdin.readline()

    if len(line.strip()) > 0:
        piid_file = line.strip()
    else:
        piid_file = default_piid_file

    if not os.path.isfile(piid_file):
        print(piid_file + " does not exist or is not a file")
        return

    print("Enter the directory you want to store the PIIDs in (<Enter> for default: ", end="")
    print(default_piid_directory + ")")
    print(">>> ", end="")
    sys.stdout.flush()
    line = sys.stdin.readline()

    global piid_directory
    if len(line.strip()) > 0:
        piid_directory = line.strip()
    else:
        piid_directory = default_piid_directory

    if os.path.exists(piid_directory):
        if not os.path.isdir(piid_directory):
            print(piid_directory + " already exists, and it isn't a directory")
            return
    else:
        os.mkdir(piid_directory)

    piid_file = open(piid_file, "r")
    piids = []
    for line in piid_file:
        piids.append(line.strip())

    global num_piids
    num_piids = len(piids)

    xss = split(piids, num_proc)
    for xs in xss:
       f = pull_gen(xs)
       t = Thread(target=f)
       t.start()

if __name__ == "__main__":
    main()
