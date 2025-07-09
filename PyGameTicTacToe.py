import pygame as PG
from pygame.locals import *
from random import randrange, choice
import Utility as ut 
import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Text, Scrollbar
import datetime
import json as js
import threading

#----------------------------------
#        SETTING PYGAME
#----------------------------------
size = 140
menuRes = (size*5, size* 5)
gatoRes = (size*3, size * 4)
clock = PG.time.Clock()
screen = PG.display.set_mode(gatoRes)

#----------------------------------
#         SETTING GAME
#----------------------------------
offset       = 0                 # Background movement
bg_color     = (0, 76, 153, 255) # Background color
players_info = ["","",0,0]       # Temporary storage of player data
game_data    = []                # Temporary storage of data to save it in text files
menu_enable  = True              # Functional menu buttons


#----------------------------------
#        LOADING SPRITES
#----------------------------------
#Loading Gato Sprites and Dictionary
gato_loads = [
    ut.load_image("Empty.png", False, (size,size)), ut.load_image("Red.png", False, (size,size)),
    ut.load_image("Green.png", False, (size,size)), ut.load_image("Circle.png", False, (size,size)),
    ut.load_image("Cross.png", False, (size,size)), ut.load_image("Interface.png", False, scale = (size * 3, size)),
    ut.load_image("Exit.png", False, (size * 0.5,size * 0.5)),ut.load_image("Again.png", False, (size * 0.5,size * 0.5))
    ]
gato_spr = {
    "Empty Tile" : gato_loads[0], "Red Tile" : gato_loads[1],
    "Green Tile" : gato_loads[2], "Circle" : gato_loads[3],
    "Cross" : gato_loads[4], "Interface" : gato_loads[5],
    "Exit" : gato_loads[6], "Again" : gato_loads[7]
}
#Loading Main Menu Sprites
mm_loads = [
    ut.load_image("Button1.png", False, scale = (size * 3.5, size *0.6)),ut.load_image("Button2.png", False, scale = (size * 3.5, size *0.6)),
    ut.load_image("Button3.png", False, scale = (size * 3.5, size *0.6)),ut.load_image("Button4.png", False, scale = (size * 3.5, size *0.6)),
    ut.load_image("Background.png", False, scale = (size, size))
]
mm_spr = {
    "Button1" : mm_loads[0], "Button2" : mm_loads[1],
    "Button3" : mm_loads[2], "Button4" : mm_loads[3],
    "Background" : mm_loads[4]
}
button_spr = [
        mm_spr["Button1"], mm_spr["Button2"],
        mm_spr["Button3"] ,mm_spr["Button4"]
        ]

#----------------------------------
#       DATA STORAGE LOGIC
#----------------------------------
# This function requests the players' names.
def Start_New_MultiplayerGame():
    global players_info

    # Start pop-up
    root = tk.Tk()
    root.withdraw()

    # Get player one name
    players_info[0] = simpledialog.askstring("", "Enter Player 1 name:")

    if players_info[0] is None or players_info[0].strip() == "":
        players_info[0] = "PLAYER1"  # Default name if the user does not enter a name
    else:
        players_info[0] = players_info[0].replace(" ", "")
        print(players_info[0])

    # Store name
    game_data.append(players_info[0])

    # Get player two name
    players_info[1] = simpledialog.askstring("", "Enter Player 2 name:")

    if players_info[1] is None or players_info[1].strip() == "":
        players_info[1] = "PLAYER2"  # Default name if the user does not enter a name
    else:
        players_info[1] = players_info[1].replace(" ", "")
        print(players_info[1])
    # Store name
    game_data.append(players_info[1])

    # Get the date data        
    x = datetime.datetime.now()
    game_data.append(x.strftime("%x")) # Date
    game_data.append(f"{x.strftime("%H")}:{x.strftime("%M")}") # Hour

    # Start multiplayer game
    Set_MP_TicTacToe() 
    
# Function responsible for saving game information at the end of the game
def Save_gameData(): 
    global game_data, players_info

    # Detect how many games already exist
    cant_games = 0
    try:
        with open("jugadores.txt", "r") as f:
            cant_games = len(f.readlines())
    except FileNotFoundError:
        with open("jugadores.txt", "w") as f:
            pass

    # Open files and save information
    with open("jugadores.txt", "a") as f:
        # Structure:[P1 NAME][P2 NAME][DATE][HOUR]
        f.write(f"[GAME {cant_games + 1}] {game_data[0]} {game_data[1]} {game_data[2]} {game_data[3]}\n")

    with open("victorias.txt", "a") as f:  # "a" = append
        f.write(f"[{cant_games + 1}] {players_info[2]} {players_info[3]}\n")

    # Reset variables for a new game.
    game_data = []
    players_info = ["","",0,0]

    # Go to menu
    SetMainMenu()

#----------------------------------
#        MAIN MENU LOGIC
#----------------------------------
def Display_Menu():
    global offset, button_spr

    # Background Settings
    screen.fill("white")
    sprite = mm_spr["Background"].copy()
    sprite.fill((bg_color), special_flags=PG.BLEND_RGBA_MULT)
    size = sprite.get_width()

    # Background Movement
    offset += 0.1
    if offset > size:
        offset = 0

    # Display Background
    for x in range(6):
        for y in range(5):
            screen.blit(sprite, [(size * x) - offset, size * y])

    # Button Settings
    texts = ["MULTIPLAYER", "VS. BOT", "HISTORY", "EXIT"]
    posy = [200, 300, 400, 500]

    # Display buttons
    for i in range(4):
        screen.blit(button_spr[i], [menuRes[0]/7, posy[i]])
        ut.draw_text(screen, texts[i], menuRes[0]/2 - 100, posy[i] + 50, (0, 0, 0), "left", 40)

    # Title
    ut.draw_text(screen, "TIC TAC TOE", menuRes[0]/2, 100, (0, 10, 43), "center", 90)
    ut.draw_text(screen, "TIC TAC TOE", menuRes[0]/2, 90, (255, 255, 255), "center", 90)
    ut.draw_text(screen,"Ignacio Loncon - Lukas Trillat",menuRes[0]/2,menuRes[1]-15,(0,0,0),"center",25)
    ut.draw_text(screen,"Ignacio Loncon - Lukas Trillat",menuRes[0]/2,menuRes[1]-19,(255,255,255),"center",25)

# Function responsible for opening the history of games played.
def Show_History():
    global menu_enable
    menu_enable = False # Disable menu buttons to avoid errors

    def Start_Window():
        try:
            # Get the stored information from "jugadores.txt" and "victorias.txt"
            data = []
            # Read documents
            with open("jugadores.txt") as f:
                player_lines = f.readlines()
            with open("victorias.txt") as w:
                wins_lines = w.readlines()

            # Store the data in the variable that will display
            for i, a in zip(player_lines, wins_lines):
                player_split = i.split()
                wins_split = a.split()
                data.append(f"{player_split[0]} {player_split[1]} - {player_split[2]} VS. {player_split[3]}\n"
                            f"{player_split[2]} WINS: {wins_split[1]}\n"
                            f"{player_split[3]} WINS: {wins_split[2]}\n"
                            f"game played on {player_split[4]} {player_split[5]}\n\n")

            # Pop-up settings
            root = tk.Tk()
            root.title("Game History")
            root.geometry("500x400")

            # Scrollbar settings
            scrollbar = tk.Scrollbar(root)
            scrollbar.pack(side="right", fill="y")
            text = tk.Text(root, yscrollcommand=scrollbar.set)
            text.pack(expand=True, fill="both")

            # Insert each line of data into the pop-up
            for line in data:
                text.insert("end", line)
            scrollbar.config(command=text.yview)

            # In case the window is closed
            def Close_Window():
                global menu_enable
                menu_enable = True
                root.destroy()

            # Close the window
            root.protocol("WM_DELETE_WINDOW", Close_Window)
            root.mainloop()

        # In case there is an error in reading the documents
        except FileNotFoundError:
            msg_root = tk.Tk()
            msg_root.withdraw()
            messagebox.showwarning("ERROR", "No games played... Play a game!")
            msg_root.destroy()

            global menu_enable
            menu_enable = True # Enable menu buttons

    #Tthe window starts without affecting the main game
    threading.Thread(target=Start_Window).start()

#----------------------------------
#       TIC TAC TOE LOGIC
#----------------------------------

#--CREATING THE BOARD--#
#List in list to create 3x3 table
board = [[r for r in range(1, 4)] for c in range(3)]
#Assignates a number to each tile
number = 1
for row in range(3):
    for column in range(3):
        board[row][column] = number
        number += 1
#Machine's first move
usedNumbers = [] #5 is always the first move of the machine

#--DISPLAYING THE BOARD--#
#Displays the base board, the "blank" tiles.
def Display_Init_Board():
    for row in range(3):
        for column in range(3):
            screen.blit(gato_spr["Empty Tile"], gato_butCoords[row][column])
#This function displays the corresponding sprites for each type of tile
def Display_Board():

    # Display board
    for row in range(3):
        for column in range(3):
            if board[row][column] == "O":
                screen.blit(gato_spr["Circle"], gato_butCoords[row][column])
            elif board[row][column] == "-":
                screen.blit(gato_spr["Red Tile"], gato_butCoords[row][column])
            elif board[row][column] == "X":
                screen.blit(gato_spr["Cross"], gato_butCoords[row][column])

    # Display current score of each player
    if gameEnd == False and actualScr == "GatoMP":
        ut.draw_text(screen,f"{players_info[0]} WINS: {players_info[2]}",gatoRes[0]/2,gatoRes[1] - 55,(0,255,0),"center",30)
        ut.draw_text(screen,f"{players_info[1]} WINS: {players_info[3]}",gatoRes[0]/2,gatoRes[1] - 20,(255,0,0),"center",30)

#--CHECKING STATUS--#
#Checking the status of the game, that could ethier continue, or end because someone won
#Check_status makes "end" true, finalizing the game, and declarating the winner
winner = None
winType = ""
finalScreen = False
moved = False
gameEnd = False

def Check_Status():
    global board, gameEnd, winner, winType, draw
    xCount = 0
    oCount = 0

    #Checks horizontal straight lines
    for row in range(3):
        #Checks the line
        for column in range(3):
            if board[row][column] == "X":
                xCount += 1
            elif board[row][column] == "O":
                oCount += 1
        #If there's three checks, someone won
        if xCount == 3:
            winner = "Glados"
            winType = "SHL"
            gameEnd = True
            return
        elif oCount == 3:
            winner = "Player"
            winType = "SHL"
            gameEnd = True
            return
        #Else, counters are reseted
        else:
            oCount = 0
            xCount = 0

    #Checks verticals stragight lines
    for column in range(3):
        for row in range(3):
            if board[row][column] == "X":
                xCount += 1
            elif board[row][column] == "O":
                oCount += 1
        #If there's three checks, someone won
        if xCount == 3:
            winner = "Glados"
            winType = "SVL"
            gameEnd = True
            return
        elif oCount == 3:
            winner = "Player"
            winType = "SVL"
            gameEnd = True
            return
        #Else, counters are reseted
        else:
            oCount = 0
            xCount = 0
            
    #Checks Diagonal Straight Lines
    if board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X":
            winner = "Glados"
            winType = "DSL(TB)"
            gameEnd = True
            return
    elif board[0][2] == "X" and board[1][1] == "X" and board[2][0] == "X":
            winner = "Glados"
            winType = "DSL(BT)"
            gameEnd = True
            return
    
    if board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O":
            winner = "Player"
            winType = "DSL(TB)"
            gameEnd = True
            return
    elif board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O":
            winner = "Player"
            winType = "DSL(BT)"
            gameEnd = True
            return
    
    #Checks for a Draw
    drawCount = 0
    for row in range(3):
        for column in range(3):
            if board[row][column] in ("X", "O"):
                drawCount += 1
    if drawCount == 9:
        winner = "Draw"
        gameEnd = True

#--AI'S MOVE--#
#The Ai "thinks", choosing a number and setting a "-" to the tile, wich is diplayed as a red tile
def GladosThink():
    global usedNumbers, playEnabled  
    playEnabled = False

    #Gets a non used number
    number = 5
    usedNumbers.sort()
    if usedNumbers == [1,2,3,4,5,6,7,8,9]:
        return
    while number in usedNumbers:
        number = randrange(1,10)

    for row in range(3):
        for column in range(3):
            if board[row][column] == number:
                screen.blit(gato_spr["Red Tile"], gato_butCoords[row][column])
                usedNumbers.append(number)
                board[row][column] = "-"
               
#After a short period of time, the "-" sets to an "X", finalizaing the AI's move and displaying the correct sprite
timeElapsed = None
resetTime = None
playEnabled = True

def GladosMove():
    global timeElapsed, resetTime, playEnabled

    if resetTime is None:
        resetTime = PG.time.get_ticks()

    timeElapsed = PG.time.get_ticks() - resetTime

    if timeElapsed >= 1000:
        for row in range(3):
            for column in range(3):
                if board[row][column] == "-":
                    PG.time.wait(1000)
                    board[row][column] = "X"  
                    playEnabled = True
                    screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3))
                    ut.draw_text(screen,"Your Turn",210,490,(0,255,0), "center", 50)    
                    PG.display.flip()
        resetTime = None

#--PLAYER'S MOVE--#
#This function is later used with the mouse position as an argument, and it returns wich tile is the mouse on
gato_butCoords = [
         [(0, 0), (gatoRes[0] / 3, 0), (gatoRes[0] / 3 * 2, 0)],
         [(0, gatoRes[1] / 4), (gatoRes[0] / 3, gatoRes[1] / 4), (gatoRes[0] / 3 * 2, gatoRes[1] / 4)],
         [(0, gatoRes[1] / 4 * 2), (gatoRes[0] / 3, gatoRes[1] / 4 * 2), (gatoRes[0] / 3 * 2, gatoRes[1] / 4 * 2)],
         ]
#This function takes the mouse position and returns the index of the tile's position
def NumberGetter(position, row = None, column = None): 

    if position[0] <= gatoRes[0] / 3 and position[0] >= 0:
        row = 0
    elif position[0] <= gatoRes[0] / 3 * 2 and position[0] >= gatoRes[0] / 3:
        row = 1
    elif position[0] <= gatoRes[0] and position[0] >= gatoRes[0] / 3 * 2:
        row = 2


    if position[1] <= gatoRes[1] / 4 and position[1] >= 1:
        column = 0
    elif position[1] <= gatoRes[1] / 4 * 2 and position[1] >= gatoRes[1] / 4 :
        column = 1
    elif position[1] <= gatoRes[1] / 4 * 3 and position[1] >= gatoRes[1] / 4 * 2:
        column = 2



    return [row,column]
#Takes the tile's number of the tile that the mouse is on, an performs the play
def PlayMove(number, type="O"):
    global usedNumbers, playEnabled, board

    # In case the Playing is disabled, returns False to avoid errors
    if not playEnabled:
        return False

    # Find the corresponding cell
    for row in range(3):
        for column in range(3):
            # Only if the box has the number we want to play
            if board[row][column] == number:
                # If it is already occupied with 'X' or 'O', we do not allow playing there.
                if board[row][column] in ("X", "O"):
                    return False

                # If it is free, we mark it with the corresponding type
                board[row][column] = type
                usedNumbers.append(number)
                return True

    return False  # Not found

def AskNewGame():
    # Function to give the player the option to play again or return to the menu
    global programEnd
    # Buttons pos
    button_pos = [
        [gatoRes[0] / 2.5 - 50, gatoRes[1] / 2 * 1.7],
        [gatoRes[0] / 2.5 + 50, gatoRes[1] / 2 * 1.7]
    ]

    # Display buttons after the game ends
    screen.blit(gato_spr["Exit"], [button_pos[0][0], button_pos[0][1]])
    screen.blit(gato_spr["Again"], [button_pos[1][0], button_pos[1][1]])
    PG.display.flip()

    #Pauses the game until the player clicks on a button
    pause = True
    while pause:
        for event in PG.event.get():
            if event.type == PG.QUIT:
                pause = False
                programEnd = True
            elif event.type == PG.MOUSEBUTTONDOWN:
                mpos = PG.mouse.get_pos()
                
                # Check if the player clicked the "Exit" button
                if button_pos[0][0] < mpos[0] < button_pos[0][0] + gato_spr["Exit"].get_width() and button_pos[0][1] < mpos[1] < button_pos[0][1] + gato_spr["Exit"].get_height():
                    pause = False
                    if actualScr == "GatoMP": #If it is multiplayer, save information
                        Save_gameData() 
                    elif actualScr == "GatoAI": # If not, return to the menu
                        SetMainMenu()

                # Check if the player clicked the "Again" button
                elif button_pos[1][0] < mpos[0] < button_pos[1][0] + gato_spr["Again"].get_width() and button_pos[1][1] < mpos[1] < button_pos[1][1] + gato_spr["Again"].get_height():
                    pause = False
                    # Reset the board
                    if actualScr == "GatoMP":
                        Set_MP_TicTacToe()
                    elif actualScr == "GatoAI":
                        Set_AI_TicTacToe()

        # Update the screen
        PG.display.flip()

#----------------------------------
#        SCREEN MANAGMENT
#----------------------------------
actualScr = "Menu"

#Sets up the main menu as the main screen, reseting the needed values
def SetMainMenu():
    global screen, actualScr, bg_color

    # Background color
    bg_color = choice([
        (230, 120, 130, 255),
        (240, 180, 100, 255),
        (240, 240, 130, 255),
        (130, 220, 160, 255),
        (130, 190, 230, 255),
        (160, 130, 230, 255),
        (230, 130, 230, 255),
    ])

    # Change Screen
    actualScr = "Menu"

    #--SETTING UP THE SCREEN--#
    screen = PG.display.set_mode(menuRes)
    PG.display.set_caption("MENU")
    screen.fill("white")
    PG.display.flip()
    
#Sets up the Tic Tac Toe Window as the main screen, reseting the needed values
def Set_AI_TicTacToe():

    global gameEnd, screen, gatoRes, gato_loads, actualScr, winner

    PG.display.flip()
    #--RESETTING VALUES--#
    actualScr = "GatoAI"
    number = 1
    for row in range(3):
        for column in range(3):
            board[row][column] = number
            number += 1
    usedNumbers.clear()
    usedNumbers.append(5)
    board[1][1] = "X"
    gameEnd = False
    winner = None

    #--SETTING UP THE SCREEN--#
    screen = PG.display.set_mode(gatoRes)
    PG.display.set_caption("This is tic tac toe!")
    screen.fill("white") #Clears the screen
    Display_Init_Board() #Displays the initial board
    screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3)) #Displays the text HUD 
    ut.draw_text(screen, "Your Turn",210,490,(0,255,0), "center", 50) #Displays the initial Text
        
    PG.display.flip()

def Set_MP_TicTacToe():
    global gameEnd, screen, gatoRes, gato_loads, actualScr, winner, currentPlayer

    PG.display.flip()
    #--RESETTING VALUES--#
    actualScr = "GatoMP"
    number = 1
    for row in range(3):
        for column in range(3):
            board[row][column] = number
            number += 1
    usedNumbers.clear()
    gameEnd = False
    winner = None
    currentPlayer = "P1"

    #--SETTING UP THE SCREEN--#
    screen = PG.display.set_mode(gatoRes)
    PG.display.set_caption("This is tic tac toe!")
    screen.fill("white") #Clears the screen
    Display_Init_Board() #Displays the initial board
    screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3)) #Displays the text HUD 
    ut.draw_text(screen, "Player 1 Turn",210,460,(0,255,0), "center", 40) #Displays the initial Text
        
    PG.display.flip()

#----------------------------------
#      TIC TAC TOE GAMELOOP
#----------------------------------
#Performs a "Turn" of the game every time the player clicks on the screen
#Also manages the following cases: -Clicking on an already used tile, -Clicking outside of the tiles
def AI_TicTacToe(event):
    global playNum, gameEnd, board, gato_loads, usedNumbers

    while True:
        playNum = NumberGetter(event.pos)

        #--GAME LOOP--#
        #If the player clicked an already used tile, the game does not continue
        Check_Status()
        if PlayMove(board[playNum[1]][playNum[0]]) == False:
            break
        #If There is a winner, the game stops
        Check_Status()
        if winner != None:
            break

        #The text screen is cleaned, and the AI plays
        screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3))
        PG.display.flip()
        ut.draw_text(screen, "Thinking",210,490,(255,0,0), "center", 50)

        #Updates the screen and calls the AI move
        PG.display.flip()
        GladosThink()
        break

def MP_TicTacToe(event):
    global playNum, gameEnd, board, gato_loads, usedNumbers, currentPlayer, playEnabled

    playEnabled = True
    while True:
        playNum = NumberGetter(event.pos)

        #--GAME LOOP--#
        #If the player clicked an already used tile, the game does not continue
        Check_Status()
        if currentPlayer == "P1":
            if PlayMove(board[playNum[1]][playNum[0]], "O") == False:
                break
        if currentPlayer == "P2":
            if PlayMove(board[playNum[1]][playNum[0]], "X") == False:
                break

        #If There is a winner, the game stops
        Check_Status()
        if winner != None:
            break

        #--PLAY PERFORMED SUCCESFULLY--#
        if currentPlayer == "P1":
            
            #The text screen is cleaned, and the text updates
            screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3))
            PG.display.flip()
            ut.draw_text(screen, "Player 2 Turn",210,460,(255,0,0), "center", 40)

            #Changes the current player and exits the loop
            currentPlayer = "P2"
            PG.display.flip()
            break

        if currentPlayer == "P2":

            #The text screen is cleaned, and the text updates
            screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3))
            PG.display.flip()
            ut.draw_text(screen, "Player 1 Turn",210,460,(0,255,0), "center", 40)

            #Changes the current player and exits the loop
            currentPlayer = "P1"
            PG.display.flip()
            break
            
#Makes the tile of the current mouse's position green, for a better game feel
def GameFeel(number, color = "Green"):
    global board

    #Changes the color to display according to the Argument given
    temp_Tile = None
    if color == "Green":
        temp_Tile = gato_spr["Green Tile"]
    elif color == "Red":
        temp_Tile = gato_spr["Red Tile"]


    #Same logic as the "DisplayBoard() function"
    for row in range(3):
        for column in range(3):
            if board[row][column] == "O":
                screen.blit(gato_spr["Circle"], gato_butCoords[row][column])
            elif board[row][column] == "X":
                screen.blit(gato_spr["Cross"], gato_butCoords[row][column])
            elif board[row][column] == number:
                screen.blit(temp_Tile, gato_butCoords[row][column])
            elif board[row][column] in (1,2,3,4,5,6,7,8,9):
                screen.blit(gato_spr["Empty Tile"], gato_butCoords[row][column])

    PG.display.flip

#----------------------------------
#          STARTS PYGAME
#----------------------------------
# Starts pygame
PG.init()
playNum = None
currentPlayer = "P1"
SetMainMenu()
programEnd = False

while not programEnd:

    for event in PG.event.get():
        #Ends the program on clicking the window's "X"
        if event.type == PG.QUIT:
            programEnd = True

        if event.type == PG.MOUSEBUTTONDOWN:
            # Interactions with menu buttons
            mpos = PG.mouse.get_pos() 
            posy = [200, 300, 400, 500]
            if menu_enable == True:
                for i in range(4):
                    # Get coordinates
                    xsc = button_spr[i].get_width()
                    ysc = button_spr[i].get_height()
                    # Depending on the button, perform some action
                    if (menuRes[0]/5 < mpos[0] < menuRes[0]/5 + xsc) and (posy[i] < mpos[1] < posy[i] + ysc):
                        if i == 0: # Multiplayer action
                            Start_New_MultiplayerGame() 
                        elif i == 1: # Vs.Bot Action
                            Set_AI_TicTacToe()
                        elif i == 2: # History Action
                            Show_History() 
                        elif i == 3: # Exit Action
                            programEnd = True  

    #Logic for the menu screen
    if actualScr == "Menu":
        Display_Menu()  
    
    #Logic for the Gato against AI
    if actualScr == "GatoAI":
        while not gameEnd:
            for event in PG.event.get():

                #Calls the Function to play every turn when click is checked
                if event.type == PG.MOUSEBUTTONDOWN:
                    try:                
                        AI_TicTacToe(event)
                    except:
                        pass
                #Calls the GameFeel Function with MouseMotion
                if event.type == PG.MOUSEMOTION:
                    playNum = NumberGetter(event.pos)
                    try:
                        GameFeel(board[playNum[1]][playNum[0]])
                    except:
                        pass
            #Every frame calls
            # -CheckStatus to determine if the game has ended
            # -Display_Board to update the board correctly
            # -GladosMove to perform the AI's move after it already check a red tile 
            Check_Status()
            Display_Board()
            GladosMove()

            PG.display.flip()
            clock.tick(60)

            #If the game has ended, then cleans the interface and
            #Prints a final text depending on the winner
            if gameEnd:
                screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3))
                PG.display.flip()

                if winner == "Player":
                    ut.draw_text(screen, "Player wins!", 210, 455, (0, 255, 0), "center", 40)
                elif winner == "Glados":
                    ut.draw_text(screen, "Glados wins!", 210, 455, (255, 0, 0), "center", 40)
                elif winner == "Draw":
                    ut.draw_text(screen, "Draw, nobody wins", 210, 455, (255, 255, 255), "center", 40)

                PG.display.flip()
                # Ask the player if they want to play another game
                AskNewGame()
                
    #Logic for the Gato Multiplayer
    if actualScr == "GatoMP":
        while not gameEnd:
            for event in PG.event.get():

                #Calls the function to play every turn when a click isis detected
                if event.type == PG.MOUSEBUTTONDOWN:
                    try:
                        MP_TicTacToe(event)
                    except:
                        pass
                #Calls the GameFeel Function with MouseMotion
                if event.type == PG.MOUSEMOTION:
                    playNum = NumberGetter(event.pos)
                    if currentPlayer == "P1":
                        try:
                            GameFeel(board[playNum[1]][playNum[0]], "Green")
                        except:
                            pass
                    elif currentPlayer == "P2":
                        try:
                            GameFeel(board[playNum[1]][playNum[0]], "Red")
                        except:
                            pass
            Check_Status()
            Display_Board()

            PG.display.flip()
            clock.tick(60)

            #If the game has ended, then cleans the interface and
            #Prints a final text depending on the winner
            if gameEnd:
                screen.blit(gato_spr["Interface"], (0, gatoRes[1] / 4 * 3))
                PG.display.flip()

                if winner == "Player":
                    ut.draw_text(screen, "Player 1 wins!", 210, 455, (0, 255, 0), "center", 40)
                    players_info[2] += 1 # award a point to the winning player
                elif winner == "Glados":
                    ut.draw_text(screen, "Player 2 wins!", 210, 455, (255, 0, 0), "center", 40)
                    players_info[3] += 1 # award a point to the winning player
                elif winner == "Draw":
                    ut.draw_text(screen, "Draw, nobody wins", 210, 455, (255, 255, 255), "center", 40)

                PG.display.flip()
                # Ask the player if they want to play another game
                AskNewGame()

    PG.display.flip()

PG.quit