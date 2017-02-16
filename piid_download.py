from subprocess import call
from threading import Thread

n = 10000000
num_proc = 100
count = 0

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
    args = ["curl", "-L", "--silent", "--referer", "\";auto\"", "-o", "piids/" + piid + ".txt", url]
    call(args)
    count += 1
    print("(" + str(count) + "/" + str(n) + ") piid " + piid + " done")

def pull_list(xs):
    for piid in xs:
        pull(piid)

def pull_gen(xs):
    return lambda: pull_list(xs)

def main():
    piid_file = open("piids.txt", "r")
    piids = []
    for line in piid_file:
        piids.append(line.strip())
    
    xss = split(piids[:n], num_proc)
    for xs in xss:
       f = pull_gen(xs)
       t = Thread(target=f)
       t.start()

if __name__ == "__main__":
    main()
