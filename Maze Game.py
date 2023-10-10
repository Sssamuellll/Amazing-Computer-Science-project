#Importing all the modules the program will be using.
import pygame
pygame.init()
from tkinter import *
from tkinter import messagebox
import random
import time

#Setting up all the variables do to with the display.
WIDTH = 500
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Amazing")
icon = pygame.image.load("amazing logo.png")
pygame.display.set_icon(icon)
FPS = 60

#Creating constant variables for all the colours I will be using.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
green = 200
blue = 255
LIGHT_BLUE = (0, green, blue)

#Assiging variables the program will be using often.
Visited = []
CoordStack = []
grid = []
x = 0
y = 0
cell = (x, y)
Choice=[]
PastChoice=[]
PastCellChoice=[]
count=0
level = 0
points= 10000000

Easy_Answered=False
Hard_Answered=False
Medium_Answered=False

SPEED=5
PLAYER_SIZE=(35, 35)
move=False

WIN.fill(WHITE)

menu_win=True
selected = "PLAY"

player_image = pygame.image.load("Player.png").convert_alpha()

#Changes the button image when called to indicate to the user that they have selected it.
def play_button(WIN, load_image):
    play_select_image = pygame.image.load("play selected.png").convert_alpha()
    play_select_image = pygame.transform.scale(play_select_image, (200, 110))
    WIN.blit(play_select_image, (150, 150))

def load_button(WIN, play_image):
    load_select_image = pygame.image.load("load selected.png").convert_alpha()
    load_select_image = pygame.transform.scale(load_select_image, (195, 110))
    WIN.blit(load_select_image, (152, 250))

def rewards_button(WIN, reward_image):
    reward_select_image = pygame.image.load("rewards button selected.png").convert_alpha()
    reward_select_image = pygame.transform.scale(reward_select_image, (183, 88))
    WIN.blit(reward_select_image, (158, 365))

#Controls how the menu looks and how the options/buttons work using key presses.
def menu(WIN, WHITE, menu_win):
    click = False
    background_image = pygame.image.load("menu background.PNG").convert_alpha()
    WIN.blit(background_image, (0, 0))
    if menu_win == True: # loads all the buttons if menu_win is true.
        play_image = pygame.image.load("play.png").convert_alpha()
        play_image = pygame.transform.scale(play_image, (200, 100))
        play_rect = pygame.draw.rect(WIN, RED, ((161, 162), (180, 80)))
        WIN.blit(play_image, (150, 150))
        load_image = pygame.image.load("load.png").convert_alpha()
        load_image = pygame.transform.scale(load_image, (195, 110))
        load_rect = pygame.draw.rect(WIN, RED, ((159, 262), (180, 88)))
        WIN.blit(load_image, (152, 250))
        reward_image = pygame.image.load("rewards button.png").convert_alpha()
        reward_image = pygame.transform.scale(reward_image, (183, 88))
        reward_rect = pygame.draw.rect(WIN, RED, ((158, 365), (180, 88)))
        WIN.blit(reward_image, (158, 365))
        selected = "PLAY"
        pygame.display.update()
        #while menu_win is true it checks the mouse for button clicks when touching with a certain button.
        while menu_win == True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #if the play button is selected these variables below will change and the main project will run.
                        if play_rect.collidepoint(mouse):
                            play_button(WIN, play_image)
                            selected = "PLAY"
                            menu_win = False
                            WIN.fill(WHITE)
                            pygame.display.update()
                            main(level, selected)
                        #if the load button is selected these variables below will change and the a previously saved maze will load. 
                        if load_rect.collidepoint(mouse):
                            load_button(WIN, load_image)
                            selected = "LOAD"
                            Loading(level, Visited, CoordStack)
                            menu_win = False
                            WIN.fill(WHITE)
                            pygame.display.update()
                            main(level, selected)
                            break
                        #if the reward button is selected the variables below will change and a new menu will appear.
                        if reward_rect.collidepoint(mouse):
                            rewards_button(WIN, reward_image)
                            selected = "REWARD"
                            Rewards_Menu(WIN)
                            break
                #if the buttons are being hovered over they will change images  to indicate they are being selected.        
                else:
                    if reward_rect.collidepoint(mouse):
                        rewards_button(WIN, reward_image)
                    else:
                        WIN.blit(reward_image, (158, 365))
                    if play_rect.collidepoint(mouse):
                        play_button(WIN, play_image)
                    else:
                        WIN.blit(play_image, (150, 150))
                    if load_rect.collidepoint(mouse):
                        load_button(WIN, load_image)
                    else:
                        WIN.blit(load_image, (152, 250))
                    pygame.display.update()
        

#Confirming the area of the maze to be drawn in which helps the maze generation generate in the correct area.
def grid_generation(WIN, x, y, grid, WHITE, BLUE, BLACK, WIDTH, HEIGHT):
    for i in range(0, int(HEIGHT/50)):
        x=0
        for j in range(0, int(WIDTH/50)):
            GridCell=(x, y)
            grid.append(GridCell)
            x = x + 50
        y = y+50

#Draws out the maze so that it leaves spaces for walls. This is called in the main maze generation subroutine.
#It looks for changes in x and y coordinates to determine what size of rectangles to draw on to the screen to form the maze.
def walls(WIN, x, y, LIGHT_BLUE, WIDTH, HEIGHT, cell, Visited, Choice):
    PastX, PastY = Visited[len(Visited)-1]
    if x < PastX:
        pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (50, 45)))#left
    if x > PastX:
        pygame.draw.rect(WIN, LIGHT_BLUE, ((x-50, y), (50, 45)))#right
    if y < PastY:
        pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (45, 50)))#up
    if y > PastY:
        pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y-50), (45, 50)))#down
    time.sleep(0.05)
    pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (45, 45)))
    pygame.draw.rect(WIN, GREEN, ((HEIGHT-50, WIDTH-50), (45, 45)))
    pygame.display.update()

#This generates the question squares in the maze after the it has been generated.
#this is called in the player_movement subroutine as it also handles collisions ultilising other subroutines.
#this subroutine check when to generate new question squares or redraw the current ones.
def Questions_Squares(WIN, HEIGHT, WIDTH, Visited, px, py, Qs_gen, occupied):
    x=0
    y=0
    coords = x, y
    square=0
    if Qs_gen == True:
        while square !=3:
            x=0
            y=0
            coords = Visited[random.randint(15, len(Visited)-1)]
            x, y = coords
            x = x +5
            y = y +5
            coords = x, y
            if coords not in occupied:
                occupied.append(coords)
                square=square+1
    if Qs_gen == False:
        easy_square_image = pygame.image.load("easy question square.png").convert_alpha()
        easy_rect = pygame.draw.rect(WIN, BLACK, ((occupied[0]), (35, 35)))
        WIN.blit(easy_square_image, (occupied[0]))
        medium_square_image = pygame.image.load("medium question square.png").convert_alpha()
        medium_rect = pygame.draw.rect(WIN, ORANGE, ((occupied[1]), (35, 35)))
        WIN.blit(medium_square_image, (occupied[1]))
        hard_square_image = pygame.image.load("hard question square.png").convert_alpha()
        hard_rect = pygame.draw.rect(WIN, RED, ((occupied[2]), (35, 35)))
        WIN.blit(hard_square_image, (occupied[2]))
        if Easy_Answered == True:
            pygame.draw.rect(WIN, LIGHT_BLUE, ((occupied[0]), (35, 35)))
        if Medium_Answered == True:
            pygame.draw.rect(WIN, LIGHT_BLUE, ((occupied[1]), (35, 35)))
        if Hard_Answered == True:
            pygame.draw.rect(WIN, LIGHT_BLUE, ((occupied[2]), (35, 35)))
        pygame.display.update()
        Questions(easy_rect, medium_rect, hard_rect, px, py)

#This subroutine determines what difficulty of question is being activated due to the type of square that has been collided with.
#The collision checks if the player representation has collided with a rect the same size as the question square previously established.
#this subroutine is called from the Question Squares subroutine if Qs_gen == False which determines whether to generate a new set
#of question squares or not.
def Questions(easy_rect, medium_rect, hard_rect, px, py):
    global Easy_Answered
    global Medium_Answered
    global Hard_Answered
    turtle=(px, py)
    if easy_rect.collidepoint(px, py) or easy_rect.collidepoint(px+35, py) or easy_rect.collidepoint(px+35, py+35) or easy_rect.collidepoint(px, py+35):
        if Easy_Answered == False:
            QType="Easy"
            Question_picker(QType)
            Easy_Answered=True
    if medium_rect.collidepoint(px, py) or medium_rect.collidepoint(px+35, py) or medium_rect.collidepoint(px+35, py+35) or medium_rect.collidepoint(px, py+35):
        if Medium_Answered == False:
            QType="Medium"
            Question_picker(QType)
            Medium_Answered=True
    if hard_rect.collidepoint(px, py) or hard_rect.collidepoint(px+35, py) or hard_rect.collidepoint(px+35, py+35) or hard_rect.collidepoint(px, py+35):
        if Hard_Answered == False:
            QType="Hard"
            Question_picker(QType)
            Hard_Answered=True

#This subroutine loads everything needed from the correct difficutly text files previously determined in the previous subroutine.
#This difficulty has been stored in the variable QType which determines what text file to open.
#certain lines from the text file is assigned to certain variables which will be used in the future.
def Question_picker(QType):
    Choices=[]
    Answer=[]
    Question=[]
    if QType == "Easy":
        Load = open("Easy.txt", "rt")
    if QType == "Medium":
        Load = open("Medium.txt", "rt")
    if QType == "Hard":
        Load = open("Hard.txt", "rt")
    
    file = Load.readlines()
    line=random.randint(1, 3)
    if line == 1:
        Question = file[0].split("#")
        Choices = file[1].split("#")
        Answer = file[2].split("#")
    if line == 2:
        Question = file[3].split("#")
        Choices = file[4].split("#")
        Answer = file[5].split("#")
    if line == 3:
        Question = file[6].split("#")
        Choices = file[7].split("#")
        Answer = file[8].split("#")
    Load.close()
    Question_Window(Choices, Answer, Question)

#This subroutine determines if this is the correct answer or not determined by the Answer list variable.
def QButton1(screen, Choices, Answer, Question):
    global points
    if Answer[0] == "1":
        points = points + 10
        screen.destroy()
        messagebox.showinfo("Correct!", "You Won 10 Points\nCurrent Points: " + str(points))
    else:
        screen.destroy()
        messagebox.showinfo("Incorrect!", "You Gained 0 Points")

#This subroutine determines if this is the correct answer or not determined by the Answer list variable.
def QButton2(screen, Choices, Answer, Question):
    global points
    if Answer[0] == "2":
        points = points + 10
        screen.destroy()
        messagebox.showinfo("Correct!", "You Won 10 Points\nCurrent Points: " + str(points))
    else:
        screen.destroy()
        messagebox.showinfo("Incorrect!", "You Gained 0 Points")

#This subroutine determines if this is the correct answer or not determined by the Answer list variable.
def QButton3(screen, Choices, Answer, Question):
    global points
    if Answer[0] == "3":
        points = points + 10
        screen.destroy()
        messagebox.showinfo("Correct!", "You Won 10 Points\nCurrent Points: " + str(points))
    else:
        screen.destroy()
        messagebox.showinfo("Incorrect!", "You Gained 0 Points")

#This subroutine loads the new window the question label and the three buttons that execute the previous three subroutines when clicked using Tkinter.
def Question_Window(Choices, Answer, Question):
    screen = Tk()
    screen.title("Amazing - Question")
    screen.geometry("500x250")
    screen.configure(bg="#1fe3ff")
    label = Label(screen, text=Question[0])
    label.place(x=250, y=75, anchor="center")
    Question_Button1=Button(screen, text=Choices[0], command=lambda: QButton1(screen, Choices, Answer, Question)).place(x=250, y=125, anchor="center")
    Question_Button2=Button(screen, text=Choices[1], command=lambda: QButton2(screen, Choices, Answer, Question)).place(x=250, y=160, anchor="center")
    Question_Button3=Button(screen, text=Choices[2], command=lambda: QButton3(screen, Choices, Answer, Question)).place(x=250, y=195, anchor="center")
    screen.mainloop()

#This subroutine is draws boundaries in the form of walls around the border of the py game window after the maze has been generated.
def Boundaries(WIN, WHITE, WIDTH, HEIGHT):
    x=-5
    y=0
    for i in range(0, WIDTH):
        pygame.draw.rect(WIN, WHITE, ((x, y), (50, 5)))
        x=x+50
    x=0
    y=-5
    for i in range(0, HEIGHT):
        pygame.draw.rect(WIN, WHITE, ((x, y), (5, 50)))
        y=y+50
    
#This subroutine is similar to the walls subroutine but is called when the load button is clicked in the main menu.
#This subroutine redraws the maze comparing the variables load from the save.txt text file using x and y coordinates.
def LoadMaze(WIN, LIGHT_BLUE, WIDTH, HEIGHT, Visited, CoordStack):
    for pos in range(0, len(Visited)):
            if pos > 0:
                PastX, PastY = Visited[pos]
                x, y = Visited[pos-1]
                pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (45, 45)))
                if x < PastX:
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (50, 45)))#left
                if x > PastX:
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((x-50, y), (50, 45)))#right
                if y < PastY:
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (45, 50)))#up
                if y > PastY:
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y-50), (45, 50)))#down
                time.sleep(0.05)
                pygame.display.update()
            else:
                pygame.draw.rect(WIN, LIGHT_BLUE, ((Visited[pos]), (45, 45)))
#This section covers the entire screen filling and missing cells that the previous algorithm missed with squares.            
    x=0
    y=0
    for i in range(0, int(HEIGHT/50)):
        x=0
        pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (45, 45)))
        pygame.display.update()
        for j in range(0, int(WIDTH/50)):
            GridCell=(x, y)
            grid.append(GridCell)
            pygame.draw.rect(WIN, LIGHT_BLUE, ((x, y), (45, 45)))
            pygame.display.update()
            x = x + 50
        y = y+50
    pygame.draw.rect(WIN, GREEN, ((HEIGHT-50, WIDTH-50), (45, 45)))
            

#This subroutine when called generates the maze in the area that has been created by the "grid_generation" subroutine.
def maze_generation(WIN, RED, BLACK, GREEN, x, y, Choice, WIDTH, HEIGHT, cell, Visited, CoordStack, count, LIGHT_BLUE):
    cell = (x, y)
    CoordStack.append(cell)
    Visited.append(cell)
    if count == 0:
        pygame.draw.rect(WIN, LIGHT_BLUE, ((0, 0), (45, 45)))
    CurrentCell=cell

#This part of the maze generation chooses what cell it should expand to next x and y using coordinates. This is completely random using randint().
    while len(Visited) < len(grid):
        while len(Choice) == 0:
            if (x+50, y) not in Visited and (x+50, y) in grid: #right
                x=x+50
                cell = (x, y)
                Choice.append(cell)
                (x, y) = CurrentCell
                PastChoice.append(cell)
            if (x-50, y) not in Visited and (x-50, y) in grid: #left
                x=x-50
                cell = (x, y)
                Choice.append(cell)
                (x, y) = CurrentCell
                PastChoice.append(cell)
            if (x, y+50) not in Visited and (x, y+50) in grid: #down
                y=y+50
                cell = (x, y)
                Choice.append(cell)
                (x, y) = CurrentCell
                PastChoice.append(cell)
            if (x, y-50) not in Visited and (x, y-50) in grid: #up
                y=y-50
                cell = (x, y)
                Choice.append(cell)
                (x, y) = CurrentCell
                PastChoice.append(cell)

#This section is ultilised when all the cells around the current cell have been visited.
#It backtracks through the maze using "CoordStack" list as a stack which pushes coordinates off the stack
#until it finds a unvisited cell and carries on. This makes it a recursive algorithm as it calls itself further down.
            if len(Choice) <= 0 and len(Visited) != len(grid):
                (x, y) = CoordStack[(len(CoordStack)-1)]
                CoordStack.remove(CoordStack[len(CoordStack)-1])

#Randomly selects from the possible choices around the current cell.
        NextCellChoice = random.randint(1, len(Choice))

#chooses the next cell determined by the randint() result and calls the walls subroutine to draw the new generated cell.
        if NextCellChoice == 1:
            pygame.draw.rect(WIN, LIGHT_BLUE, ((Choice[0]), (45, 45)))
            (x, y) = Choice[0]
            cell = x, y
            walls(WIN, x, y, LIGHT_BLUE, WIDTH, HEIGHT, cell, Visited, Choice)
            
        if NextCellChoice == 2:
            pygame.draw.rect(WIN, LIGHT_BLUE, ((Choice[1]), (45, 45)))
            (x, y) = Choice[1]
            cell = x, y
            walls(WIN, x, y, LIGHT_BLUE, WIDTH, HEIGHT, cell, Visited, Choice)

        if NextCellChoice == 3:
            pygame.draw.rect(WIN, LIGHT_BLUE, ((Choice[2]), (45, 45)))
            (x, y) = Choice[2]
            cell = x, y
            walls(WIN, x, y, LIGHT_BLUE, WIDTH, HEIGHT, cell, Visited, Choice)
            
        if NextCellChoice == 4:
            pygame.draw.rect(WIN, LIGHT_BLUE, ((Choice[3]), (45, 45)))
            (x, y) = Choice[3]
            cell = x, y
            walls(WIN, x, y, LIGHT_BLUE, WIDTH, HEIGHT, cell, Visited, Choice)

#Updates display to draw on the chosen cell and clears Choices for the next cell selection.  
        pygame.display.update()
        del Choice[:]
        count=count+1
#calls the algortithm again to repeat the process making this section a recursive algorithm.
        maze_generation(WIN, RED, BLACK, GREEN, x, y, Choice, WIDTH, HEIGHT, cell, Visited, CoordStack, count, LIGHT_BLUE)

#When called this subroutine resets certain variables so that they can be used again when generating the next maze.
def reset(Visited, CoordStack, grid, x, y):
    global Easy_Answered
    global Medium_Answered
    global Hard_Answered
    Easy_Answered=False
    Medium_Answered=False
    Hard_Answered=False
    del Visited[:]
    del CoordStack[:]
    del grid[:]
    x=0
    y=0

#When the rewards button is clicked this menu subroutine is called.
def Rewards_Menu(WIN):
    WIN.fill(LIGHT_BLUE)
    menu=True
#loads in all the images needed and draws all the rectangles that are going to be interacted with as buttons.
    background_image = pygame.image.load("rewards backdrop.png").convert_alpha()
    WIN.blit(background_image, (0, 0))
    inventory_image = pygame.image.load("inventory.png").convert_alpha()
    inventory_image = pygame.transform.scale(inventory_image, (250, 88))
    inventory_rect = pygame.draw.rect(WIN, RED, ((125, 365), (250, 88)))
    inv_select_image = pygame.image.load("inventory selected.png").convert_alpha()
    inv_select_image = pygame.transform.scale(inv_select_image, (250, 88))
    chest_image = pygame.image.load("chest closed.png").convert_alpha()
    chest_rect = pygame.draw.rect(WIN, RED, ((175, 230), (158, 100)))
    exit_image = pygame.image.load("exit.png").convert_alpha()
    exit_image = pygame.transform.scale(exit_image, (50, 60))
    exit_select_image = pygame.image.load("exit selected.png").convert_alpha()
    exit_select_image = pygame.transform.scale(exit_select_image, (50, 60))
    exit_rect = pygame.draw.rect(WIN, RED, ((432, 417), (30, 48)))
    WIN.blit(chest_image, (0, 0))
    WIN.blit(exit_image, (420, 410))
#while true the algorithm checks whether the mouses is clicking a button. 
    while menu == True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #if the inventory button is clicked then the rewards inventory subroutine will be called.
                    if inventory_rect.collidepoint(mouse):
                        Rewards_inventory(WIN, exit_image, exit_select_image, chest_image)
                    #if the chest is called then the rewards chest subroutine will be called.
                    if chest_rect.collidepoint(mouse):
                        Rewards_chest(WIN, background_image, chest_image, exit_image, exit_select_image)
                    #if exit_rect is clicked then the while loop will stop which forces the menu back to the main menu.
                    if exit_rect.collidepoint(mouse):
                        background_image = pygame.image.load("menu background.PNG").convert_alpha()
                        WIN.blit(background_image, (0, 0))
                        menu=False
            #if the mouse is hovering over the rewards button then a different image will blit to indicate that it has been selected.
            else:
                if chest_rect.collidepoint(mouse):
                    reward_text=pygame.freetype.Font("Gameplay.ttf", 20)
                    reward_text.render_to(WIN, (150, 190), "Unlock rewards!", (WHITE))
                else:
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((150, 190), (250, 20)))
                if inventory_rect.collidepoint(mouse):
                    WIN.blit(inv_select_image, (125, 365))
                else:
                    WIN.blit(inventory_image, (125, 365))
                if exit_rect.collidepoint(mouse):
                    WIN.blit(exit_select_image, (420, 410))
                else:
                    WIN.blit(exit_image, (420, 410))
        pygame.display.update()

#When called this subroutine handles if the chest clicked and what happens when it is.
def Rewards_chest(WIN, background_image, chest_image, exit_image, exit_select_image):
    ClickCount=0
    InvOrChest="CHEST"
    WIN.fill(LIGHT_BLUE)
    reward_text=pygame.freetype.Font("Gameplay.ttf", 20)
    global points
    rewards_menu=True
    #loads in all the images needed for this menu screen.
    chest_open_image = pygame.image.load("chest open.png").convert_alpha()
    WIN.blit(background_image, (0, 0))
    chest_rect = pygame.draw.rect(WIN, RED, ((175, 230), (158, 100)))
    WIN.blit(chest_image, (0, 0))
    exit_rect = pygame.draw.rect(WIN, RED, ((432, 417), (30, 48)))
    WIN.blit(exit_image, (420, 410))
    #while true this checks if the mouse is clicking certain buttons that are determined through use of rectangles.
    while rewards_menu == True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #if the chest is clicked then points will be retracted, the turtle assets subroutine is called and the rest
                    #is creating a mini animation to show the user they won something.
                    if chest_rect.collidepoint(mouse):
                        if points >= 100:
                            pygame.draw.rect(WIN, LIGHT_BLUE, ((140, 50), (250, 200)))
                            points = points - 100
                            WIN.blit(chest_open_image, (0, 0))
                            Turtle_Assets(InvOrChest, ClickCount)
                            pygame.display.update()
                            time.sleep(2)
                            pygame.draw.rect(WIN, LIGHT_BLUE, ((140, 50), (250, 200)))
                            pygame.draw.rect(WIN, LIGHT_BLUE, ((50, 50), (500, 50)))
                            WIN.blit(chest_image, (0, 0))
                        # if the user does not have enough points the text below will explain this to them.
                        else:
                            reward_text.render_to(WIN, (140, 100), "Not enough points!", (RED))
                            pygame.display.update()
                            time.sleep(2)
                            pygame.draw.rect(WIN, LIGHT_BLUE, ((140, 100), (250, 20)))
                    # the exit button works the same as before but this time it will take you back to the rewards menu not the main menu.
                    if exit_rect.collidepoint(mouse):
                        background_image = pygame.image.load("rewards backdrop.png").convert_alpha()
                        WIN.blit(background_image, (0, 0))
                        WIN.blit(chest_image, (0, 0))
                        rewards_menu=False
            # if the mouse is hovering over the rectangles/buttons then the images will change to indicate if the user is selecting them.                
            else:
                if chest_rect.collidepoint(mouse):
                    reward_text.render_to(WIN, (150, 170), "Unlock rewards,", (WHITE))
                    reward_text.render_to(WIN, (160, 190), "For 100 points!", (WHITE))
                else:
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((150, 170), (250, 50)))
                if exit_rect.collidepoint(mouse):
                    WIN.blit(exit_select_image, (420, 410))
                else:
                    WIN.blit(exit_image, (420, 410))
        pygame.display.update()

#This subroutine is called when the inventory button is clicked.
def Rewards_inventory(WIN, exit_image, exit_select_image, chest_image):
    InvOrChest="INVENTORY"
    inv_menu=True
    ClickCount=0
    WIN.fill(LIGHT_BLUE)
    #loads in all the images needed in this algorithm for this menu
    x_rect=pygame.draw.rect(WIN, RED, ((150, 350), (75, 75)))
    tick_rect=pygame.draw.rect(WIN, RED, ((275, 350), (75, 75)))
    x_image = pygame.image.load("reward dequip.png").convert_alpha()
    x_select_image = pygame.image.load("reward dequip selected.png").convert_alpha()
    WIN.blit(x_image, (150, 350))
    tick_image = pygame.image.load("reward equip icon.png").convert_alpha()
    tick_select_image = pygame.image.load("reward equip icon selected.png").convert_alpha()
    WIN.blit(tick_image, (275, 350))
    arrow_image = pygame.image.load("reward arrow.png").convert_alpha()
    arrow_select_image = pygame.image.load("reward arrow selected.png").convert_alpha()
    pygame.draw.rect(WIN, WHITE, ((150, 150), (200, 200)))
    pygame.draw.rect(WIN, LIGHT_BLUE, ((165, 165), (170, 170)))
    arrow1_rect=pygame.draw.rect(WIN, RED, ((360, 225), (30, 55)))
    WIN.blit(arrow_image, (300, 175))
    exit_rect = pygame.draw.rect(WIN, RED, ((432, 417), (30, 48)))
    WIN.blit(exit_image, (420, 410))
    #while true this checks whether several different buttons have been clicked using rectangles.
    while inv_menu == True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #checks if the arrow to the right of the square in the middle has been clicked
                    #if so then tutle assests subroutine will be called
                    if arrow1_rect.collidepoint(mouse):
                        ClickCount=ClickCount+1
                        Turtle_Assets(InvOrChest, ClickCount)
                    #the exit button does the same as previously stated in the rewards chest subroutine.
                    if exit_rect.collidepoint(mouse):
                        WIN.fill(LIGHT_BLUE)
                        background_image = pygame.image.load("rewards backdrop.png").convert_alpha()
                        WIN.blit(background_image, (0, 0))
                        WIN.blit(chest_image, (0, 0))
                        inv_menu=False
                    #checks if the unequip button has been clicked. calls the turtle assets subroutine.
                    if x_rect.collidepoint(mouse):
                        InvOrChest = "UNEQUIP"
                        Turtle_Assets(InvOrChest, ClickCount)
                    #checks if the equip button has been clicked. calls the turtle assets subroutine.
                    if tick_rect.collidepoint(mouse):
                        InvOrChest="EQUIP"
                        Turtle_Assets(InvOrChest, ClickCount)
            # checks if the mouse is hovering over the previously stated buttons and changes the images to indicate that they have been selected.
            else:
                if arrow1_rect.collidepoint(mouse):
                    WIN.blit(arrow_select_image, (300, 175))
                else:
                    WIN.blit(arrow_image, (300, 175))
                if exit_rect.collidepoint(mouse):
                    WIN.blit(exit_select_image, (420, 410))
                else:
                    WIN.blit(exit_image, (420, 410))
                if x_rect.collidepoint(mouse):
                    WIN.blit(x_select_image, (150, 350))
                else:
                    WIN.blit(x_image, (150, 350))
                if tick_rect.collidepoint(mouse):
                    WIN.blit(tick_select_image, (275, 350))
                else:
                    WIN.blit(tick_image, (275, 350))
        pygame.display.update()

#when called this subroutine load up all the different turtle rewards ready to be using in different algortithms.
def Turtle_Assets(InvOrChest, ClickCount):
    turtle_assests=[]
    turtles=["Monochrome Turtle", "Pink Turtle", "Pirate Turtle", "Red Demon Scyth Turtle", "Blue Turtle", "British Turtle"]
    turtle_mono = pygame.image.load("monochrome turtle.png").convert_alpha()
    turtle_pink = pygame.image.load("pink turtle.png").convert_alpha()
    turtle_pirate = pygame.image.load("pirate turtle.png").convert_alpha()
    turtle_RDS = pygame.image.load("red demon cypth turtle.png").convert_alpha()
    turtle_blue = pygame.image.load("blue turtle.png").convert_alpha()
    turtle_uk = pygame.image.load("british turtle.png").convert_alpha()
    turtle_assests.append(turtle_mono)
    turtle_assests.append(turtle_pink)
    turtle_assests.append(turtle_pirate)
    turtle_assests.append(turtle_RDS)
    turtle_assests.append(turtle_blue)
    turtle_assests.append(turtle_uk)
    #checks what button has been clicked and calls the corrosponding subroutine.
    if InvOrChest=="CHEST":
        Chest_Open(WIN, turtles, turtle_assests, turtle_mono, turtle_pink, turtle_pirate, turtle_RDS, turtle_blue, turtle_uk)
    if InvOrChest=="INVENTORY":
        Inv_Arrow(WIN, turtles, turtle_assests, turtle_mono, turtle_pink, turtle_pirate, turtle_RDS, turtle_blue, turtle_uk, ClickCount, InvOrChest)
    if InvOrChest=="EQUIP":
        Inv_Arrow(WIN, turtles, turtle_assests, turtle_mono, turtle_pink, turtle_pirate, turtle_RDS, turtle_blue, turtle_uk, ClickCount, InvOrChest)
    if InvOrChest=="UNEQUIP":
        Unequip(WIN, turtles, turtle_assests, turtle_mono, turtle_pink, turtle_pirate, turtle_RDS, turtle_blue, turtle_uk)

#This is called when the inventory button has been clicked.
#if scrolls through the different turtles the user has previously unlocked that are held in the text file.
def Inv_Arrow(WIN, turtles, turtle_assests, turtle_mono, turtle_pink, turtle_pirate, turtle_RDS, turtle_blue, turtle_uk, ClickCount, InvOrChest):
    #loads the text file.
    load = open("Unlocked_Turtles.txt", "rt")
    file = load.readlines()
    if len(file)>0:
        unlocked=file[0].split("#")
        if ClickCount <= len(unlocked):
            turtle_selected=unlocked[ClickCount-1]
            for pos in range(0, len(turtles)):
                if turtle_selected==turtles[pos]:
                    turtle_selected=turtle_assests[pos]
                    #equips the current turtle presented in the square.
                    if InvOrChest=="EQUIP":
                        Equip(turtle_selected)
                    else:
                        turtle_image = pygame.transform.scale(turtle_selected, (150, 150))
                        pygame.draw.rect(WIN, LIGHT_BLUE, ((165, 165), (170, 170)))
                        WIN.blit(turtle_image, (170, 170))

#when called this subroutine reassigns the original turtle images to the player image variable.
def Unequip(WIN, turtles, turtle_assests, turtle_mono, turtle_pink, turtle_pirate, turtle_RDS, turtle_blue, turtle_uk):
    global player_image
    player_image = pygame.image.load("Player.png").convert_alpha()

#changes the player variable to the current turtle presented in the square.
def Equip(turtle_selected):
    global player_image
    player_image=turtle_selected

#when the chest is clicked, this subroutine is called.
def Chest_Open(WIN, turtles, turtle_assests, turtle_mono, turtle_pink, turtle_pirate, turtle_RDS, turtle_blue, turtle_uk):
    global points
    text_placements=[75, 165, 155, 50, 165, 150]
    turtle_text=pygame.freetype.Font("Gameplay.ttf", 27)
    load = open("Unlocked_Turtles.txt", "rt")
    file = load.readlines()
    Save=False
    locked=True
    unlocked_turtles=[]
    while locked==True:
        turtle_found=False
        Save=False
        #chooses a random turtle for the list of turtles using randint().
        turtle=random.randint(0, 5)
        turtle_won=turtles[turtle]

        #check if turtle is saved in text file.
        if len(file)>0:
            unlocked=file[0].split("#")

        #saving textfile to list to rewrite.
            for position in range(0, len(unlocked)-1):
                unlocked_turtles.append(unlocked[position])

        #check if turtle is saved in text file.
            for pos in range(0, len(unlocked)-1):
                if turtle_won == unlocked[pos]:

                    turtle_found=True
            if turtle_found==False:
                Save=True
            locked=False
        else:
            locked=False
            Save=True
    #if no turtle is found then it proceeds to unlock the turtle won form the chest.
    if turtle_found==False:
        unlocked_turtles.append(turtle_won)
        turtle_won=turtle_assests[turtle]
        turtle_image = pygame.transform.scale(turtle_won, (150, 150))
        WIN.blit(turtle_image, (175, 75))
        turtle_won=turtles[turtle]
        text_placements[turtle]
        turtle_text.render_to(WIN, (text_placements[turtle-2], 50), turtle_won, (WHITE))
    else:
        turtle_text=pygame.freetype.Font("Gameplay.ttf", 20)
        turtle_text.render_to(WIN, (120, 50), "ALL TURTLES UNLOCKED", (RED))
        points=points+100
    if Save == True:
        save = open("Unlocked_Turtles.txt", "wt")
        for i in range(0, len(unlocked_turtles)):
            save.write(str(unlocked_turtles[i]+"#"))    

#Will controll how big the maze is and keeps track of what level the user is on.
def Levels(level, WIN):
    global WIDTH
    global HEIGHT
    global LIGHT_BLUE
    global green
    global blue
    #changes the size of the maze once the user has create level equivilent to a multiple of ten.
    if level % 10 == 0:
        HEIGHT = HEIGHT + 50
        WIDTH = WIDTH + 50
    if green > 0 and blue > 0:
        green = green-5
        blue = blue-5
    LIGHT_BLUE = (0, green, blue)
    level_text=pygame.freetype.Font("Gameplay.ttf", 40)
    level_text.render_to(WIN, (150, 200), "Level "+str(level), (LIGHT_BLUE))
    pygame.display.update()
    time.sleep(0.5)
    return(WIDTH, HEIGHT, LIGHT_BLUE)

#Saves the relevent data into a text file called "Save" so that the same maze can be loaded again. This is called after each maze has generated.
def saving(level, Visited, CoordStack):
    global points
    Save = open("Save.txt", "wt")
    Save.write(str(level) + "\n")
    for j in range(0, len(CoordStack)):
         Coordinate = CoordStack[j]
         Save.write(str(Coordinate)+"#")
    Save.write("\n")
    for i in range(0, len(Visited)):
         Visit = Visited[i]
         Save.write(str(Visit)+"#")
    Save.write("\n"+str(points))
    Save.close()

#This will eventually load the maze saved in the textfile through the use of the "LOAD" option in the menu.
def Loading(level, Visited, CoordStack):
    global points
    x=0
    y=0
    Load = open("Save.txt", "rt")
    file = Load.readlines()
    level = file[0]
    Visited_list=file[2:3]
    Visited_str = Visited_list[0]
    PartsofVisited = Visited_str.split("#")
    #load the information from the text file from a string back into integer tuples
    for pos in range(0, len(PartsofVisited)-1):
        Part=PartsofVisited[pos]
        Parts=Part.split(",")
        x=Parts[0][1:len(Parts[0])]
        y=Parts[1][0:len(Parts[1])-1]
        cell=(int(x), int(y))
        Visited.append(cell)
    #load the information from the text file back into integer tuples from a string.
    CoordStack_str=file[1]
    PartsofCoordStack = CoordStack_str.split("#")
    for position in range(0, len(PartsofCoordStack)-1):
        CoordStack_Part=PartsofCoordStack[position]
        CoordStack_Parts=CoordStack_Part.split(",")
        x=CoordStack_Parts[0][1:len(CoordStack_Parts[0])]
        y=CoordStack_Parts[1][0:len(CoordStack_Parts[1])-1]
        cell=(int(x), int(y))
        CoordStack.append(cell)

    points=file[len(file)]

#Controls the movement of the player, how it collides with the walls and the end cell and draws the player in the new location.
def player_movement(WIN, BLACK, playerstate, SPEED, PLAYER_SIZE, move, HEIGHT, WIDTH, LIGHT_BLUE):
    py=5
    px=5
    leftmove=False
    rightmove=False
    downmove=False
    upmove=False
    occupied =[]

    turtle = pygame.transform.rotate(player_image, 0)
    
    WIN.blit(turtle, (px, py))
    pygame.display.update()
    Qs_gen=True
    #calls this subroutine to load the question squares.
    Questions_Squares(WIN, HEIGHT, WIDTH, Visited, px, py, Qs_gen, occupied)
    Qs_gen = False
    while playerstate == True:
        if WIN.get_at((px+34, py)) == (0, 255, 0) or WIN.get_at((px+34, py+34)) == (0, 255, 0):#determines if the player is touching the end.
            reset(Visited, CoordStack, grid, x, y)
            break
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            Questions_Squares(WIN, HEIGHT, WIDTH, Visited, px, py, Qs_gen, occupied)
            if keys_pressed[pygame.K_a]: #LEFT
                turtle = pygame.transform.rotate(player_image, 90)
                if WIN.get_at((px, py)) == (255, 255, 255) or WIN.get_at((px-1, py+34)) == (255, 255, 255): #determines if the player is touching a wall.
                    #moves the player if not touching a wall in the ideal direction
                    leftmove = False
                else:
                    leftmove = True
                if leftmove == True:
                    #removes and redraws the turtle in the new position
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((px, py), (PLAYER_SIZE)))
                    px=px-SPEED
                    WIN.blit(turtle, (px, py))
                pygame.display.update()

            if keys_pressed[pygame.K_d]: #RIGHT
                turtle = pygame.transform.rotate(player_image, -90)
                if WIN.get_at((px+35, py)) == (255, 255, 255) or WIN.get_at((px+34, py+34)) == (255, 255, 255):#determines if the player is touching a wall.
                    #moves the player if not touching a wall in the ideal direction
                    rightmove = False
                else:
                    rightmove = True
                if rightmove == True:
                    #removes and redraws the turtle in the new position
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((px, py), (PLAYER_SIZE)))
                    px=px+SPEED
                    WIN.blit(turtle, (px, py))
                pygame.display.update()

            if keys_pressed[pygame.K_s]: #DOWN
                turtle = pygame.transform.rotate(player_image, 180)
                if WIN.get_at((px, py+35)) == (255, 255, 255) or WIN.get_at((px+34, py+34)) == (255, 255, 255):#determines if the player is touching a wall.
                    #moves the player if not touching a wall in the ideal direction
                    downmove = False
                else:
                    downmove = True
                if downmove == True:
                    #removes and redraws the turtle in the new position
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((px, py), (PLAYER_SIZE)))
                    py=py+SPEED
                    WIN.blit(turtle, (px, py))
                pygame.display.update()

            if keys_pressed[pygame.K_w]: #UP
                turtle = pygame.transform.rotate(player_image, 0)
                if WIN.get_at((px, py-5)) == (255, 255, 255) or WIN.get_at((px+34, py-5)) == (255, 255, 255):#determines if the player is touching a wall.
                    #moves the player if not touching a wall in the ideal direction.
                    upmove = False
                else:
                    upmove = True
                if upmove == True:
                    #removes and redraws the turtle in the new position
                    pygame.draw.rect(WIN, LIGHT_BLUE, ((px, py), (PLAYER_SIZE)))
                    py=py-SPEED
                    WIN.blit(turtle, (px, py))
        pygame.display.update()

#The main subroutine that controls the whole game e.g. the exit window button and all the subroutines.
def main(level, selected):
    pygame.display.quit()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Amazing")
    clock = pygame.time.Clock()
    run = True
    while run:
        #recreates the py game window which is relevent after the level is equal to a multiple of ten
        pygame.display.quit()
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Amazing")
        icon = pygame.image.load("amazing logo.png")
        pygame.display.set_icon(icon)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        playerstate = False
        level = level + 1
        WIN.fill(WHITE)
        Levels(level, WIN)
        grid_generation(WIN, x, y, grid, WHITE, BLUE, BLACK, WIDTH, HEIGHT)
        pygame.display.quit()
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Amazing")
        pygame.display.set_icon(icon)
        WIN.fill(WHITE)
        pygame.display.update()
        if selected == "PLAY":
            maze_generation(WIN, RED, BLACK, GREEN, x, y, Choice, WIDTH, HEIGHT, cell, Visited, CoordStack, count, LIGHT_BLUE)
        else:
            LoadMaze(WIN, LIGHT_BLUE, WIDTH, HEIGHT, Visited, CoordStack)
        pygame.display.update()
        Boundaries(WIN, WHITE, WIDTH, HEIGHT)
        saving(level, Visited, CoordStack)
        playerstate = True
        player_movement(WIN, BLACK, playerstate, SPEED, PLAYER_SIZE, move, HEIGHT, WIDTH, LIGHT_BLUE)
        WIN.fill(WHITE)
            
    pygame.quit()

menu(WIN, WHITE, menu_win)
if __name__ == "__main__":
    main(level, selected)
