import sys
sys.dont_write_bytecode = True

with open("warp_pts.txt") as f:
    pts = []
    for line in f:
        line = line.rstrip("\n")
        l = line.split(" ")
        pts.append((int(l[0]), int(l[1])))

print(pts)