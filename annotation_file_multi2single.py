import sys

input_filename = sys.argv[1]
output_filename = sys.argv[2]

with open(input_filename, "r") as f:
    inputlines = f.read().splitlines()

fw = open(output_filename, mode = "w")
for n in range(len(inputlines)):
    l = inputlines[n].split(" ")
    if len(l) < 1:
        continue
    filenames = l[0]

    for i in range(len(l) - 1):
        p = l[i + 1]
        if len(p.split(",")) < 4:
            continue
        print(filenames, p, file = fw)
fw.close()