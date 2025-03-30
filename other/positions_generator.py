from random import shuffle

# starting position
with open("../positions/pos1.txt") as pos1:
    position = [line[:-1].split(" ") for line in pos1]

# mid-game positions
for i in range(99):
    to_write = ""
    shuffle(position)
    for row in position:
        shuffle(row)
        for x in row:
            to_write += x + " "
        to_write = to_write[:-1] + "\n"
    with open(f"positions/pos{i+2}.txt", "w") as new_position:
        new_position.write(to_write)
