# This file define what exists in the world.
import glob, copy, json
from libraries import *
from engine import *

# CREATE A DICTIONARY READING FILES IN A FOLDER
# FilesToDict(*Path, ValidExt, If is room then put yes if not let blank)
def FilesToDict(Path, Ext, IsRoom='no'):
    ListOfFiles = glob.glob(Path + '*' + Ext)
    ListOfFilesB = copy.copy(ListOfFiles)

    if IsRoom.lower() == "yes":
        for n, i in enumerate(ListOfFilesB):
            a = i.replace(Path,'')
            b = a.replace(Ext,'')
            ListOfFilesB[n] = b

        for n, i in enumerate(ListOfFilesB):
            try:
                int(i)
            except ValueError:
                ListOfFiles.pop(n)

    Dict = {}

    for i in ListOfFiles:
        fileread = open(i,"r")
        thisfile = fileread.readlines()
        fileread.close()
        for i in thisfile:
            thisfile[0] = thisfile[0].replace('\n','')
            if IsRoom.lower() == "yes":
                thisfile[1] = thisfile[1].replace('\n','')
                thisfile[2] = thisfile[2].replace('\n','')
        thisfilelist = list(thisfile)
        if IsRoom.lower() == "yes":
            thisfilelist[1] = json.loads(thisfilelist[1])
        Dict[thisfilelist[0]] = thisfilelist[1:]

    return Dict

# SHOW ROOM DESCRIPTION TO PLAYER IN FRIENDLY FORMAT
# ShowRoom(FilesToDict(RoomsPath, ValidExt, 'yes'),'1')
# Rooms = rooms dictionary
# Number = specific room number (ID)
def ShowRoom(Rooms, Number):
    result = ' '.join(list(Rooms[Number][0]))
    return prcolor(6, Rooms[Number][1]) + '\n[ Exits: ' + prcolor(7, result) + ' ]\n' + ' '.join(Rooms[Number][2:])

# Defines default paths and valid extension for files
RoomsPath = './rooms/'
ObjectsPath = './objects/'
ValidExt = '.txt'

# Create subdirectories if don't exist
if os.path.isdir(RoomsPath) is False:
    os.mkdir(RoomsPath)
if os.path.isdir(ObjectsPath) is False:
    os.mkdir(ObjectsPath)

# OBJECTS
# Read folder "objects" and create dictionary reading files in there
# name: (look, touch, use)
BaseObjectsDic = FilesToDict(ObjectsPath, ValidExt)
# Void final dictionary of objects
ObjectsDic = {}
# Fulfill final dictionary of objects (object name: atribute 1, attribute 2 etc)
for i in BaseObjectsDic:
# name: Class(name, look, touch, use)
    ObjectsDic[i] = SudObject(i,BaseObjectsDic[i][0],BaseObjectsDic[i][1],BaseObjectsDic[i][2])

# ROOMS
# Read folder "rooms" and create dictionary reading files in there
# IDs : (Exits, Room title, Room description)
BaseRoomsDic = FilesToDict(RoomsPath, ValidExt, 'yes')
# Void final dictionary of rooms
RoomsDic = {}
# Fulfill final dictionary of rooms
for i in BaseRoomsDic:
    desc = ShowRoom(BaseRoomsDic, i)
# 'ID' : Class(string: Room title, Exits, Room description)
# To call an area, use 'ID'
    RoomsDic[i] = SudArea(desc)

# Attaching interactive stuff to areas
RoomsDic['1'].addObject('flower', ObjectsDic['rose']) # porto
RoomsDic['2'].addObject('crap', ObjectsDic['poo']) # praia
RoomsDic['3'].addObject('fruit', ObjectsDic['apple']) # alfandega
RoomsDic['4'].addObject('bird', ObjectsDic['sparrow']) # donzela

# Link all areas with bidirectional references automatically
for key in RoomsDic:
    directions = BaseRoomsDic[key][0]
    for j in directions:
        if j == "n":
            j2 = "north"
        elif j == "s":
            j2 = "south"
        elif j == "e":
            j2 = "east"
        elif j == "w":
            j2 = "west"
        RoomsDic[key].addArea(j2, RoomsDic[directions[j]])

# Create a character
char = SudPlayer('Temporary Name')

# Create a game with player and starting area
game = SudGame(char, RoomsDic['1'])

# Lets go!
#ClearScreen()
game.run()
