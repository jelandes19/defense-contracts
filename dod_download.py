from multiprocessing import Process
from threading import Thread
import requests
import sys
import os
import shutil

base_url = "http://archive.defense.gov/Contracts/Contract.aspx?ContractID="
directory = "./dod_raw_html"
n = 5605
contract_ids = list(range(1, n + 1))
num_proc = 20
texts = {}
count = 0

def split(xs, n):
    xss = []
    for i in range(n):
        xss.append([])
    for i in range(len(xs)):
        j = i % n
        xss[j].append(xs[i])
    return xss

def pull(cid, folder, file_name):
    url = base_url + str(cid)
    r = requests.get(url)
    global count
    count += 1
    print("(" + str(count) + "/" + str(n) + "): ", end="")
    if r.status_code != 200:
        print("Error getting contract id: " + str(cid) + " (Error: " + str(r.status_code) + ")")
    else:
        print("Got contract id: " + str(cid))
        f = open(folder + "/" + file_name, "w")
        f.write(r.text)
        f.close()

def pull_list(xs):
    for cid in xs:
        pull(cid, directory, str(cid) + ".html")

def pull_gen(xs):
    return lambda: pull_list(xs)

def main():
    global directory
    print("This program will download the DoD defense contracts archive.")
    print("Enter to directory to store the files (Press <Enter> for default: \"" + directory + "\")")
    print(">>> ", end="")
    sys.stdout.flush()
    line = sys.stdin.readline()
    if len(line.strip()) > 0:
        directory = line.strip()

    print("dir = \"" + directory + "\"")
    # Create dir
    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)

    jobs = split(contract_ids, num_proc)
    funcs = [pull_gen(job) for job in jobs]
    for f in funcs:
        t = Thread(target=f)
        t.start()

    """
    for cid_list in split(contract_ids, 5):
        print(cid_list)
        for cid in cid_list:
            pull(cid, directory, str(cid) + ".html")
    for cid in contract_ids:
        print("Getting contract id: " + str(cid))
        url = base_url + str(cid)
        r = requests.get(url)
        if r.status_code != 200:
            print("Error getting contract id: " + str(cid) + " (Error: " + str(r.status_code) + ")")
        else:
            texts[cid] = r.text

    print("There are " + str(len(texts)) + " documents")
    """

if __name__ == "__main__":
    main()
