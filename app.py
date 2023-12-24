import cv2
import numpy as np 
from array import *
from operator import itemgetter
import matplotlib.pyplot as plt
import math
import random
import os
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request, render_template, send_file, current_app, send_from_directory

app = Flask(__name__, static_url_path='/static')

board_path = 'training/TestBoard.png'
tree_path = 'training/TreeNew.png'
brick_path = 'training/BrickNew.png'
sheep_path = 'training/SheepNew.png'
wheat_path = 'training/WheatNew.png'
ore_path = 'training/OreNew.png'
desert_path = 'training/DesertNew.png'
num2_path = 'training/2.png'
num3_path = 'training/3.png'
num4_path = 'training/4.png'
num5_path = 'training/5.png'
num6_path = 'training/6.png'
num8_path = 'training/8.png'
num9_path = 'training/9.png'
num10_path = 'training/10.png'
num11_path = 'training/11.png'
num12_path = 'training/12.png'

tiles = []
rarity_odds = [0, 0, 1, 2, 3, 4, 5, 0, 5, 4, 3, 2, 1, 0, 0]

#mapping of adjacent hexagons
adjacencies =[
    [1,3,4],
    [0,2,4,5],
    [1,5,6],
    [0,4,7,8],
    [0,1,3,5,8,9],
    [1,2,4,6,9,10],
    [2,5,10,11],
    [3,8,12],
    [3,4,7,9,12,13],
    [4,5,8,10,13,14],
    [5,6,9,11,14,15],
    [6,10,15],
    [7,8,13,16],
    [8,9,12,14,16,17],
    [9,10,13,15,17,18],
    [10,11,14,18],
    [12,13,17],
    [13,14,16,18],
    [14,15,17]
]

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#   FLASK
#----------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/generate_board', methods=['POST'])
def generate_board():
    # Clears the spots
    global gui_spots
    gui_spots = []
    # Generate the board
    new_tiles = generate_fair_board()
    BoardImage(new_tiles)

    image_path = 'static/generated_image.png'
    return jsonify({'image_path': image_path})

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#   BOARD GENERATOR
# Generates a random board list
# Ex. output: 
# [['wheat', 9], ['ore', 12], ['desert', 0], ['brick', 3], 
# ['wheat', 11], ['wheat', 11], ['ore', 5], ['ore', 8], 
# ['brick', 8], ['tree', 10], ['brick', 2], ['wheat', 3], 
# ['tree', 5], ['sheep', 4], ['sheep', 10], ['tree', 6], 
# ['tree', 4], ['sheep', 6], ['sheep', 9]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def generate_board():
    board = []
    resources = [['tree', 4], ['brick', 3], ['sheep', 4], ['wheat', 4], ['ore', 3], ['desert', 1]]
    rarities = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]

    for i in range(19):
        random_resource = random.choice(resources)

        while random_resource[1] == 0:
            random_resource = random.choice(resources)

        if random_resource[0] == 'desert':
            random_rarity = 0
        else:            
            random_rarity = random.choice(rarities)


        board.append([random_resource[0], random_rarity])
        
        random_resource[1] -= 1
        if random_resource[0] != 'desert':
            rarities.remove(random_rarity)

    return board

#----------------------------------------------------------------------------------------------------------------------------------------------------------
# FAIR BOARD GENERATOR
#----------------------------------------------------------------------------------------------------------------------------------------------------------

def check_fairness(board):
    for i in range(19):
        for j in adjacencies[i]:
            if(board[i][1] == 6 and board[j][1] == 6 or board[i][1] == 8 and board[j][1] == 6 or board[i][1] == 6 and board[j][1] == 8 or board[i][1] == 8 and board[j][1] == 8):
                return False
    return True

def generate_fair_board():
    board = generate_board()
    while(not check_fairness(board)):
        board = generate_board()
    return board
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#   BOARD VIEWER
# Generates a board list of tiles that is able to be analyzed given a screenshot of a board from colonist.io
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def BoardViewer():
    threshold = .80

    board = [[None for _ in range(5)] for _ in range(5)]

    rarities = []
    placement_spots = []
    rarity_points = [0] * 5
    rarity_percentage = [0] * 5

    xDiff = 40
    yDiff = 70

    class Tile:
        def __init__(self, location, resource, rarity):
            self.location = location
            self.resource = resource
            self.rarity = rarity
        
        def __str__(self):
            return f"{self.location}, {self.resource}, {self.rarity}"

    board_img = cv2.imread(board_path, cv2.IMREAD_UNCHANGED)

    #cv2.imshow('Board', board_img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    # Finds all of the tiles for the material passed as a parameter
    def findTiles(path, label=None):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(board_img, img, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        w = img.shape[1]
        h = img.shape[0]

        yloc, xloc = np.where(result >= threshold)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, .2)

        print("" + path + ": ")
        print(len(rectangles))

        coords = []

        for (x, y, w, h) in rectangles:
            cv2.rectangle(board_img, (x,y), (x + w, y + h), (0,255,255), 2)
            if isinstance(label, str):
                tiles.append([x, y, label])
            else:
                rarities.append([x, y, label])


    findTiles(tree_path, "tree")
    findTiles(brick_path, "brick")
    findTiles(sheep_path, "sheep")
    findTiles(wheat_path, "wheat")
    findTiles(ore_path, "ore")
    findTiles(desert_path, "desert")

    threshold = .95

    findTiles(num2_path, 2)
    findTiles(num3_path, 3)
    findTiles(num4_path, 4)
    findTiles(num5_path, 5)
    findTiles(num6_path, 6)
    findTiles(num8_path, 8)
    findTiles(num9_path, 9)
    findTiles(num10_path, 10)
    findTiles(num11_path, 11)
    findTiles(num12_path, 12)


    #cv2.imshow('Board', board_img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    tiles.sort(key=itemgetter(1))

    for t in tiles:
        print(t)

    for r in rarities:
        print(r)

    tiles[:3] = sorted(tiles[:3])
    tiles[3:7] = sorted(tiles[3:7])
    tiles[7:12] = sorted(tiles[7:12])
    tiles[12:16] = sorted(tiles[12:16])
    tiles[16:19] = sorted(tiles[16:19])


    print("______New________")

    for t in tiles:
        print(t)


    for r in rarities:
        for t in tiles:
            if abs(r[0] - t[0]) < xDiff and abs(r[1] - t[1]) < yDiff:
                t.append(r[2])
                
    min(tiles, key=len).append(0)

    print("______Newest________")
    for t in tiles:
        print(t)

    def setup_placements():
        placement_spots.append([tiles[0][2:]])
        placement_spots.append([tiles[0][2:]])
        placement_spots.append([tiles[0][2:], tiles[1][2:]])
        placement_spots.append([tiles[1][2:]])
        placement_spots.append([tiles[1][2:], tiles[2][2:]])
        placement_spots.append([tiles[2][2:]])
        placement_spots.append([tiles[2][2:]])

        placement_spots.append([tiles[3][2:]])
        placement_spots.append([tiles[0][2:], tiles[3][2:]])
        placement_spots.append([tiles[0][2:], tiles[3][2:], tiles[4][2:]])
        placement_spots.append([tiles[0][2:], tiles[1][2:], tiles[4][2:]])
        placement_spots.append([tiles[1][2:], tiles[4][2:], tiles[5][2:]])
        placement_spots.append([tiles[1][2:], tiles[2][2:], tiles[5][2:]])
        placement_spots.append([tiles[2][2:], tiles[5][2:], tiles[6][2:]])
        placement_spots.append([tiles[2][2:], tiles[6][2:]])
        placement_spots.append([tiles[6][2:]])

        placement_spots.append([tiles[7][2:]])
        placement_spots.append([tiles[3][2:], tiles[7][2:]])
        placement_spots.append([tiles[3][2:], tiles[7][2:], tiles[8][2:]])
        placement_spots.append([tiles[3][2:], tiles[4][2:], tiles[8][2:]])
        placement_spots.append([tiles[4][2:], tiles[8][2:], tiles[9][2:]])
        placement_spots.append([tiles[4][2:], tiles[5][2:], tiles[9][2:]])
        placement_spots.append([tiles[5][2:], tiles[9][2:], tiles[10][2:]])
        placement_spots.append([tiles[5][2:], tiles[6][2:], tiles[10][2:]])
        placement_spots.append([tiles[6][2:], tiles[10][2:], tiles[11][2:]])
        placement_spots.append([tiles[6][2:], tiles[11][2:]])
        placement_spots.append([tiles[11][2:]])

        placement_spots.append([tiles[7][2:]])
        placement_spots.append([tiles[7][2:], tiles[12][2:]])
        placement_spots.append([tiles[7][2:], tiles[8][2:], tiles[12][2:]])
        placement_spots.append([tiles[8][2:], tiles[12][2:], tiles[13][2:]])
        placement_spots.append([tiles[8][2:], tiles[9][2:], tiles[13][2:]])
        placement_spots.append([tiles[9][2:], tiles[13][2:], tiles[14][2:]])
        placement_spots.append([tiles[9][2:], tiles[10][2:], tiles[14][2:]])
        placement_spots.append([tiles[10][2:], tiles[14][2:], tiles[15][2:]])
        placement_spots.append([tiles[10][2:], tiles[11][2:], tiles[15][2:]])
        placement_spots.append([tiles[11][2:], tiles[15][2:]])
        placement_spots.append([tiles[11][2:]])

        placement_spots.append([tiles[12][2:]])
        placement_spots.append([tiles[12][2:], tiles[16][2:]])
        placement_spots.append([tiles[12][2:], tiles[13][2:], tiles[16][2:]])
        placement_spots.append([tiles[13][2:], tiles[16][2:], tiles[17][2:]])
        placement_spots.append([tiles[13][2:], tiles[14][2:], tiles[17][2:]])
        placement_spots.append([tiles[14][2:], tiles[17][2:], tiles[18][2:]])
        placement_spots.append([tiles[14][2:], tiles[15][2:], tiles[18][2:]])
        placement_spots.append([tiles[15][2:], tiles[18][2:]])
        placement_spots.append([tiles[15][2:]])
        
        placement_spots.append([tiles[16][2:]])
        placement_spots.append([tiles[16][2:]])
        placement_spots.append([tiles[16][2:], tiles[17][2:]])
        placement_spots.append([tiles[17][2:]])
        placement_spots.append([tiles[17][2:], tiles[18][2:]])
        placement_spots.append([tiles[18][2:]])
        placement_spots.append([tiles[18][2:]])


    setup_placements()

    print("Done::::")

    for p in placement_spots:
        print(p)

    print(rarity_points)

    for t in tiles:
        if t[2] == "tree":
            print(t[3])
            rarity_points[0] += rarity_odds[t[3]]
        elif t[2] == "brick":
            print(t[3])
            rarity_points[1] += rarity_odds[t[3]]
        elif t[2] == "sheep":
            print(t[3])
            rarity_points[2] += rarity_odds[t[3]]
        elif t[2] == "wheat":
            print(t[3])
            rarity_points[3] += rarity_odds[t[3]]
        elif t[2] == "ore":
            print(t[3])
            rarity_points[4] += rarity_odds[t[3]]
        
    print("rarity points:")
    for r in rarity_points:
        print(r)

    def calculate_rarity(type):
        if type == "tree":
            return round(100 * rarity_points[0]/58)
        elif type == "brick":
            return round(100 * rarity_points[1]/58)
        elif type == "sheep":
            return round(100 * rarity_points[2]/58)
        elif type == "wheat":
            return round(100 * rarity_points[3]/58)
        elif type == "ore":
            return round(100 * rarity_points[4]/58)


    print(rarity_points)

    rarity_percentage[0] = calculate_rarity("tree")
    rarity_percentage[1] = calculate_rarity("brick")
    rarity_percentage[2] = calculate_rarity("sheep")
    rarity_percentage[3] = calculate_rarity("wheat")
    rarity_percentage[4] = calculate_rarity("ore")

    print(calculate_rarity("tree"))
    print(calculate_rarity("brick"))
    print(calculate_rarity("sheep"))
    print(calculate_rarity("wheat"))
    print(calculate_rarity("ore"))


    labels = ['Tree', 'Brick', 'Sheep', 'Wheat', 'Ore']

    colors =['green', 'darkorange', 'lightgreen', 'yellow', 'gray']

    plt.pie(rarity_percentage, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')

    plt.axis('equal')

    #plt.show()
'''
Track the resources and values for each placement spot
Options to rank by:
    Straight resource production
    Resource production taking into account resource scarcity
'''

def rank_by_production_straight(spots_to_rank):
    production = []

    # Straight
    for s in spots_to_rank:
        total_production = 0
            
        for x in s[1:]:
            total_production += rarity_odds[0 if x[1] == '' else int(x[1])]

        production.append(total_production)

    return production

'''          
def rank_by_production_scarcity():
    production = []
    # Scarcity
    for p in placement_spots:
        total_production = 0

        for x in p:
            total_production += rarity_odds[x[1]]

        production.append(total_production)
    
    return [production]
'''


#----------------------------------------------------------------------------------------------------------------------------------------------------------
# Image Generator
#----------------------------------------------------------------------------------------------------------------------------------------------------------
gui_spots = []

def hexagonMaker(new_tiles,side_length,center_x, center_y, i):
    rotation_angle_deg = 30  # Angle in degrees

    # Calculate rotated hexagon vertices
    rotation_angle_rad = math.radians(rotation_angle_deg)
    hexagon_vertices = [
    (
        center_x + (x - center_x) * math.cos(rotation_angle_rad) - (y - center_y) * math.sin(rotation_angle_rad),
        center_y + (x - center_x) * math.sin(rotation_angle_rad) + (y - center_y) * math.cos(rotation_angle_rad)
    )
    for x, y in [
        (center_x + side_length * x, center_y + side_length * y)
        for x, y in [
            (-1, 0), (-0.5, -0.87), (0.5, -0.87),
            (1, 0), (0.5, 0.87), (-0.5, 0.87)
        ]
    ]
    ]

 
    fill_color = ""
    if(new_tiles[i][0]=='tree'):
        fill_color = 'green'
    elif(new_tiles[i][0]=='brick'):
        fill_color = 'darkorange'
    elif(new_tiles[i][0]=='sheep'):
        fill_color = 'lightgreen'
    elif(new_tiles[i][0]=='wheat'):
        fill_color = 'yellow'
    elif(new_tiles[i][0]=='ore'):
        fill_color = 'gray'
    else:
        fill_color = (200, 180, 130)

    if(new_tiles[i][1] != 0):
        return(hexagon_vertices, fill_color, str(new_tiles[i][1]))
    else:
        return(hexagon_vertices, fill_color, "")
    
    
def dotDrawer(x, y, number, draw):
    dot_size = 8
    
    text_color = 'red' if number in ('6', '8') else 'black'

    if number != '' and rarity_odds[eval(number)] == 1:
        draw.ellipse([(x - dot_size*2 + dot_size*1.5, y + 20), 
                  (x + dot_size - dot_size*2 + dot_size*1.5, y + dot_size + 20)],
                 fill = text_color)
    elif number != '' and rarity_odds[eval(number)] == 2:
        for i in range(0, 2):
            draw.ellipse([(x - dot_size*2*i + dot_size*.5, y + 20), 
                  (x + dot_size - dot_size*2*i + dot_size*.5, y + dot_size + 20)],
                 fill = text_color)
    elif number != '' and rarity_odds[eval(number)] == 3:
        for i in range(0, 3):
            draw.ellipse([(x - dot_size*2*i + dot_size*1.5, y + 20), 
                  (x + dot_size - dot_size*2*i + dot_size*1.5, y + dot_size + 20)],
                 fill = text_color)
    elif number != '' and rarity_odds[eval(number)] == 4:
        for i in range(0, 4):
            draw.ellipse([(x - dot_size*2*i + dot_size*2.5, y + 20), 
                  (x + dot_size - dot_size*2*i + dot_size*2.5, y + dot_size + 20)],
                 fill = text_color)
    elif number != '' and rarity_odds[eval(number)] == 5:
        for i in range(0, 5):
            draw.ellipse([(x - dot_size*2*i + dot_size*3.5, y + 20), 
                  (x + dot_size - dot_size*2*i + dot_size*3.5, y + dot_size + 20)],
                 fill = text_color)
    
# Gets the coordinates of each placement spot and puts all of the placement spots in gui_spots as sorted list
def placementCoordinates(all_hexagon_vertices, draw):
    spot_size = 20

    for a in all_hexagon_vertices:
        for v in a[0]:
            check_other_spot = False
            x = v[0]
            y = v[1]
        
            for s in gui_spots:
                if abs(x - s[0][0]) <= 30 and abs(y - s[0][1]) <= 30:
                    check_other_spot = True
                    s.append([a[1], a[2]])
            
            if not check_other_spot:
                gui_spots.append([[x, y], [a[1], a[2]]])
                
    gui_spots.sort(key=lambda x: x[0][1])
    
    gui_spots[:7] = sorted(gui_spots[:7])
    gui_spots[7:16] = sorted(gui_spots[7:16])
    gui_spots[16:27] = sorted(gui_spots[16:27])
    gui_spots[27:38] = sorted(gui_spots[27:38])
    gui_spots[38:47] = sorted(gui_spots[38:47])
    gui_spots[47:54] = sorted(gui_spots[47:54])
            
            
    for g in gui_spots[1:]:
        for i in g:
            if(i[0] == 'green'):
                i[0] = 'tree'
            elif(i[0] == 'darkorange'):
                i[0] = 'brick'
            elif(i[0] == 'lightgreen'):
                i[0] = 'sheep'
            elif(i[0] == 'yellow'):
                i[0] = 'wheat'
            elif(i[0] == 'gray'):
                i[0] = 'ore'
            elif(i[0] == (200, 180, 130)):
                i[0] = 'desert'
    
    for g in gui_spots:
        print(g)
        
    
    
def spotDrawer(draw):
    spot_size = 20
    
    visualizeProductionRaw(spot_size, draw)
    
    
def visualizeProductionRaw(spot_size, draw):
    production = rank_by_production_straight(gui_spots)
    
    for p in production:
        print(p)
        
    for i in range(0, len(gui_spots)):
        draw.ellipse([(gui_spots[i][0][0] - spot_size/2, gui_spots[i][0][1] - spot_size/2), 
                      (gui_spots[i][0][0] + spot_size/2, gui_spots[i][0][1] + spot_size/2)],
                     fill = (255 - production[i] * 17, production[i] * 17, 0))
    

def BoardImage(new_tiles):
    print(new_tiles)
    side_length = 100
    img = Image.new("RGB", (1200, 1200), "blue")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    halfHexxy = side_length*math.sin(math.radians(60)) #half hex width
    all_hexagon_vertices = []

    for i in range (0,3):
        verts,color,number = hexagonMaker(new_tiles, side_length, 
                                          425 + (2*halfHexxy + (halfHexxy/10)) * i, 
                                          250, i)
        all_hexagon_vertices.append([verts, color, number])
        draw.polygon(verts, fill=color)
        text_color = 'red' if number in ('6', '8') else 'black'
        draw.text((425 + (2*halfHexxy + (halfHexxy/10)) * i, 250), 
                  number, anchor = 'mm', font = font, fill = text_color)
        dotDrawer(425 + (2*halfHexxy + (halfHexxy/10)) * i, 250, number, draw)
    for i in range (0,4):
        verts,color,number = hexagonMaker(new_tiles, side_length, 
                                          (425-halfHexxy-(halfHexxy/20)) + ((2*halfHexxy + (halfHexxy/10))*i), 
                                          250+2*(halfHexxy-(halfHexxy/10)), (i+3))
        all_hexagon_vertices.append([verts, color, number])
        draw.polygon(verts, fill=color)
        text_color = 'red' if number in ('6', '8') else 'black'
        draw.text(((425-halfHexxy-(halfHexxy/20)) + ((2*halfHexxy + (halfHexxy/10))*i), 250+2*(halfHexxy-(halfHexxy/10))), 
                  number, anchor = 'mm', font = font, fill=text_color)
        dotDrawer((425-halfHexxy-(halfHexxy/20)) + ((2*halfHexxy + (halfHexxy/10))*i), 250+2*(halfHexxy-(halfHexxy/10)), number, draw)
    for i in range (0,5):
        verts,color,number = hexagonMaker(new_tiles, side_length, 
                                          (425-2*halfHexxy-(halfHexxy/10)) + (2*halfHexxy + (halfHexxy/10))*i, 
                                          250+4*(halfHexxy-(halfHexxy/10)), (i+7))
        all_hexagon_vertices.append([verts, color, number])
        draw.polygon(verts, fill=color)
        text_color = 'red' if number in ('6', '8') else 'black'
        draw.text(((425-2*halfHexxy-(halfHexxy/10)) + (2*halfHexxy + (halfHexxy/10))*i, 250+4*(halfHexxy-(halfHexxy/10))), 
                  number, anchor = 'mm', font = font, fill=text_color)
        dotDrawer((425-2*halfHexxy-(halfHexxy/10)) + (2*halfHexxy + (halfHexxy/10))*i, 250+4*(halfHexxy-(halfHexxy/10)), number, draw)
    for i in range (0,4):
        verts,color,number = hexagonMaker(new_tiles, side_length, 
                                          (425-halfHexxy-(halfHexxy/20))+(2*halfHexxy + (halfHexxy/10))*i, 
                                          250+6*(halfHexxy-(halfHexxy/10)), (i+12))
        all_hexagon_vertices.append([verts, color, number])
        draw.polygon(verts, fill=color)
        text_color = 'red' if number in ('6', '8') else 'black'
        draw.text(((425-halfHexxy-(halfHexxy/20))+(2*halfHexxy + (halfHexxy/10))*i, 250+6*(halfHexxy-(halfHexxy/10))), 
                  number, anchor = 'mm', font = font, fill=text_color)
        dotDrawer((425-halfHexxy-(halfHexxy/20))+(2*halfHexxy + (halfHexxy/10))*i, 250+6*(halfHexxy-(halfHexxy/10)), number, draw)
    for i in range (0,3):
        verts,color,number = hexagonMaker(new_tiles, side_length, 
                                          425+(2*halfHexxy + (halfHexxy/10))*i, 
                                          250+8*(halfHexxy-(halfHexxy/10)), (i+16))
        all_hexagon_vertices.append([verts, color, number])
        draw.polygon(verts, fill=color)
        text_color = 'red' if number in ('6', '8') else 'black'
        draw.text((425+(2*halfHexxy + (halfHexxy/10))*i, 250+8*(halfHexxy-(halfHexxy/10))), 
                  number, anchor = 'mm', font = font, fill=text_color)
        dotDrawer(425+(2*halfHexxy + (halfHexxy/10))*i, 250+8*(halfHexxy-(halfHexxy/10)), number, draw)
    
    placementCoordinates(all_hexagon_vertices, draw)
    spotDrawer(draw)
    img.save("static/generated_image.png")

'''  
def main():
    BoardViewer()
    new_tiles = generate_fair_board()
    BoardImage(new_tiles)



main()
'''  