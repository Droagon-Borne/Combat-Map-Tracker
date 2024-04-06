import os

from math import floor, ceil

from PIL import Image

# Opens image - Local File in repl.it
baseMap = Image.open('map.jpg')

# Rescale image size down, if needed
width = baseMap.width
height = baseMap.height

#Monster Sizes
sizes = {
    "T": [4/3, 2.6],
    "S": [1.2, 2.75],
    "M": [1, 3],
    "L": [1, 7, 2],
    "H": [1, 11, 3],
    "G": [1, 15, 4]
}

#clears the Console
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()


#Helps read data from text files
def separate(dataBlock):
    word = ""
    all_words = []
    for dat in dataBlock:
        for letter in dat:
            if letter == ";":
                all_words.append(word)
                word = ""
            else:
                word += letter
    return all_words


#Removes unwanted items from a word
def remove(word, items):
    new = ""
    letters = []
    for l in word:
        letters.append(l)
    for l in letters:
        for i in items:
            if l == i:
                letters.remove(l)
    for l in letters:
        new += l
    return new


#Asks questions efficiently
def ask(question, answers=("Y", "N"), exceptions=None):
    while True:
        ask = str(input(question + "\n"))
        for answer in answers:
            if ask == str(answer):
                return answer
            if ask == str(exceptions):
                return ask
        if answers == "num":
            try:
                return int(ask)
            except:
                pass
        print("Please enter a valid answer.")


#Makes a grid on a specified image
def make_grid(map_base):
    global width, height

    #Gets the spacing of the grid
    num_squares_width = int(input("How many squares width-wise?\n"))
    column_spacing = round(map_base.width / num_squares_width)
    rows_spacing = column_spacing

    #Records square size
    with open("data.txt", "r+") as data:
        data.write(str(column_spacing) + ";")

    #Sets up the new image's pixel array
    all_pixels = []
    map = map_base.getdata()

    #duplicates the image for editing
    for pixl in map:
        all_pixels.append(pixl)

    listLocation = 0
    imageXY = [0, 0]

    while listLocation < len(all_pixels):
        #If the current pixel is within 2 pixels of a designated grid line, 
        #it changes the pixel's color to black
        if imageXY[0] % column_spacing <= 1 or imageXY[1] % rows_spacing <= 1:
            all_pixels[listLocation] = (0, 0, 0)

        #tracks location in image
        imageXY[0] += 1
        listLocation += 1
        if imageXY[0] == width:
            imageXY[0] = 0
            imageXY[1] += 1

    #Returns the new image
    updated = Image.new("RGB", map_base.size)
    updated.putdata(all_pixels)
    return updated


#Reads the spacing of the squares
with open("data.txt", "r") as data:
    dataBanks = data.readlines()
    dataBanks = separate(dataBanks)
    squareSpace = int(dataBanks[0])
    squ = squareSpace / 2


#Gets the location of the pixels of a square of a particular size 
#and at a particular coordinate
def loc(x, y, size="M"):
    global width, squareSpace, sizes, squ
    currentSize = sizes[size]

    #Gets important variables 
    #(x-1 because grid is from 1->x)
    x = (x - 1) * squareSpace
    y = (y - 1) * squareSpace
    pixls = []
    #Calculates distance from border of square
    squX = squ * 0.5 * currentSize[0]
    squY = floor(squX) + 1

    if size == "M" or size == "S" or size == "T":
        #determines area of square if it is Medium or smaller
        squSize = round(squareSpace-(2*squX))
        squSize = squSize*squSize
        squX = round(squX)
    else:
        #determines area of the square if it is Large or larger
        squSize = (squareSpace * currentSize[2]) - (2 * squY)
        squSize *= squSize
        squX = round(squX)

    #For every pixel in the square, it adds that pixel's location to pixls
    for pixel in range(int(squSize)):
        squX += 1
        pixls.append(int(x + round(squX) + ((y + squY) * width)))

        #if the current line is finished, it resets to a new line
        #if squX is equal to the width of the square plus squX
        if squX == ceil(currentSize[1] * round(squareSpace * 0.25)):
            squX = round(squ * 0.5 * currentSize[0])
            squY += 1
    return pixls


#If a gridded map doesn't exist, it makes one and saves it
if not os.path.exists("mapGrid.jpg"):
    updated_map = make_grid(baseMap)
    updated_map.save("mapGrid.jpg")
    clearConsole()
griddedMap = Image.open("mapGrid.jpg")


#Draws monsters at those coordinates
def drawMonsters(coordinates, colors):
    
    #Gets the griddedMap's data
    global griddedMap
    pixels = []
    map = griddedMap.getdata()

    #Copies that data
    for pix in map:
        pixels.append(pix)

    which_monster = 0
    #Then, at these specific locations, changes its color to the designated color
    for cList in coordinates:
        for xy in cList:
            pixels[xy] = tuple(colors[which_monster])
        which_monster += 1

    #Returns the new image
    updated = Image.new("RGB", griddedMap.size)
    updated.putdata(pixels)
    return updated


#Retrieves the information for a certain monster
def getMonster(isCharacter=False):
    global ask, squareSpace, width, height, separate

    #Creates the correct answers for coordinates
    answersX = []
    for num in range(int(width / squareSpace + 1)):
        answersX.append(num + 1)
    answersY = []
    for num in range(int(height / squareSpace + 1)):
        answersY.append(num + 1)

    #Asks for coordinates
    coordinateX = int(ask("What is the X coordinate of the beast?", answersX))
    coordinateY = int(ask("What is the Y coordinate of the beast?", answersY))

    #If they are a character, it gives them their color automatically
    if isCharacter is not False:
        color = isCharacter

    else:
        #Retrieves the color in correct format
        color = separate(
            input("Color in data.txt format please. Ex: 205;23;0;\n"))
        for item in range(len(color)):
            color[item] = int(color[item])

    #Gets the size and HP of the monster, unless they are a character
    if isCharacter is False:
        size = ask("""What's the creature's size?
(T)iny, (S)mall, (M)edium, (L)arge, (H)uge, (G)argantuan""",
                   ["T", "S", "M", "L", "H", "G"])
        HP = ask("How much HP does this creature have?", "num")
        return [coordinateX, coordinateY, size, color, HP]
    
    #If the creature is a character, it automatically does the following
    else:
        size = "M"
        return [coordinateX, coordinateY, size, color]


characters = {
    dataBanks[1]: (int(dataBanks[2]), int(dataBanks[3]), int(dataBanks[4])),
    dataBanks[5]: (int(dataBanks[6]), int(dataBanks[7]), int(dataBanks[8])),
    dataBanks[9]: (int(dataBanks[10]), int(dataBanks[11]), int(dataBanks[12])),
    dataBanks[13]:
    (int(dataBanks[14]), int(dataBanks[15]), int(dataBanks[16])),
    dataBanks[17]: (int(dataBanks[18]), int(dataBanks[19]), int(dataBanks[-1]))
}
