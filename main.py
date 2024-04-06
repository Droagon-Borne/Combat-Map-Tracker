import functions

#I can either slowly create every monster/player or us mData
creatures = {}
quickORslow = str(functions.ask(
    "Quick or slow? Y for Quick, N for slow.")).upper()
if quickORslow == "N":
    currentEncounter = "PREP"
else:
    #Reads the creatures in mData
    with open("mData.txt", "r") as data:
        ms = data.readlines()
        ms = functions.separate(ms)
    for item in range(int(round(len(ms) / 8))):
        c = item * 8
        creatures[ms[c]] = [  #Assigned to name
            int(ms[c + 1]),  #X
            int(ms[c + 2]),  #Y
            ms[c + 3],  #Size
            (int(ms[c + 4]), int(ms[c + 5]), int(ms[c + 6])),  #RGB
            int(ms[c + 7])  #HP
        ]
    currentEncounter = "RUNNING"


#Prepares the encounter with...
while currentEncounter == "PREP":
    state = "C"
    
	#Characters first
    while state == "C":
        #if they answer yes it moves on to monsters
        all = functions.ask("Will all the characters be joining?")
        functions.clearConsole()

        if all == "Y" or all == "YES":
            ch = functions.characters.keys()
            state = "M"

        #If there are only some characters, the code will get them as a list 
        #via "separate" before moving on to monsters
        else:
            state = "W"
            num_of_characters = 0

            while state == "W":
                ch = functions.separate(
                    input(
                        """Specify which characters in the following format:
                        CHANCY;BLUE;SNOWBALL;\n"""
                    ))
                state = "M"
                functions.clearConsole()

        #adds characters to creature dictionary
        for c in ch:
            print(c, ":\n")
            creatures[c] = functions.getMonster(tuple(functions.characters[c]))
        functions.clearConsole()

    #While on monsters, it asks how many monsters there are(1),
    #their sizes, colors, and their coordinates(2)
    while state == "M":
        amount = int(input("How many monsters are there?\n"))  #(1)

        #For every monster, it creates one under that number
        for monster in range(amount):
            print("Monster number {}:\n".format(monster + 1))
            creatures[monster] = functions.getMonster()  #!!!MAKE SURE TO MAKE HP
            functions.clearConsole()
        state = None
        currentEncounter = "RUNNING"


#While the encounter runs, it first draws, asks who moves where/dies, 
#repeat until done
while currentEncounter == "RUNNING":
    
#Gets all the locations and colors of each creature before 
#drawing each of them and saving them as the current map
    list_of_locs = []
    list_of_clrs = []
    
    for cr in creatures:
        list_of_locs.append(
            functions.loc(creatures[cr][0], creatures[cr][1], creatures[cr][2]))
        list_of_clrs.append(creatures[cr][3])
    current_map = functions.drawMonsters(list_of_locs, list_of_clrs)
    current_map.save("currentMap.jpg")

    #For each creature, it lists its name and current coordinates
    count = 1
    for key in creatures:
        print("{}. {} [{}, {}] HP: {}".format(
            count, key, creatures[key][0], creatures[key][1], creatures[key][0]))
        #Creature number, its name, X and Y coordinates, and its HP
        count += 1

    #Allows the editing of a sngle creature's locations and HP
    current, x, y, HP = functions.separate(
                            str(input(
"""Enter the following for a creatures turn, in this format:
NAME;xCHANGE;yCHANGE;hpCHANGE;(if any)\n\n""")
                    )
    )
    creatures[current][0] += int(x)
    creatures[current][1] -= int(y)
    creatures[current][4] += int(HP)
    if creatures[current][4] <= 0: #deletes the creature if HP <= 0
        del creatures[current]
    functions.clearConsole()
