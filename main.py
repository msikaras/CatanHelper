import cv2
import numpy as np 
from array import *
from operator import itemgetter
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw

board_path = 'TestBoard.png'
tree_path = 'TreeNew.png'
brick_path = 'BrickNew.png'
sheep_path = 'SheepNew.png'
wheat_path = 'WheatNew.png'
ore_path = 'OreNew.png'
desert_path = 'DesertNew.png'
num2_path = '2.png'
num3_path = '3.png'
num4_path = '4.png'
num5_path = '5.png'
num6_path = '6.png'
num8_path = '8.png'
num9_path = '9.png'
num10_path = '10.png'
num11_path = '11.png'
num12_path = '12.png'

tiles = []

#----------------------------------------------------------------------------------------------------------------------------------------------------------
# BOARD VIEWER
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def BoardViewer():
    threshold = .80

    board = [[None for _ in range(5)] for _ in range(5)]

    rarities = []
    placement_spots = []
    rarity_points = [0] * 5
    rarity_odds = [0, 0, 1, 2, 3, 4, 5, 0, 5, 4, 3, 2, 1, 0, 0]
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


    cv2.imshow('Board', board_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

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

    plt.show()

    '''
    Track the resources and values for each placement spot
    Options to rank by:
        Straight resource production
        Resource production taking into account resource scarcity
    '''

    def rank_by_production_straight():
        production = []

        # Straight
        for p in placement_spots:
            total_production = 0
                
            for x in p:
                total_production += rarity_odds[x[1]]

            production.append([p, total_production])

        return [production]
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

    for p in rank_by_production_straight():
        print(p)

    #print(rank_by_production_scarcity())

    for p in placement_spots:
        print(p)

    print("test")

def hexagonMaker(side_length,center_x, center_y, i):
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
    if(tiles[i][2]=='tree'):
        fill_color = 'green'
    elif(tiles[i][2]=='brick'):
        fill_color = 'darkorange'
    elif(tiles[i][2]=='sheep'):
        fill_color = 'lightgreen'
    elif(tiles[i][2]=='wheat'):
        fill_color = 'yellow'
    elif(tiles[i][2]=='ore'):
        fill_color = 'gray'
    else:
        fill_color = 'beige'

    return(hexagon_vertices, fill_color)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------
# GUI
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def BoardGUI(tiles):
    print(tiles)
    side_length = 100
    img = Image.new("RGB", (1200, 1200), "blue")
    draw = ImageDraw.Draw(img)
    halfHexxy = side_length*math.sin(math.radians(60)) #half hex width

    for i in range (0,3):
        verts,color = hexagonMaker(side_length,400+(10+2*halfHexxy)*i,200, i)
        draw.polygon(verts, fill=color)
    for i in range (0,4):
        verts,color = hexagonMaker(side_length,(400-halfHexxy-5)+((10+2*halfHexxy)*i),200+2*(halfHexxy-5), (i+3))
        draw.polygon(verts, fill=color)
    for i in range (0,5):
        verts,color = hexagonMaker(side_length,(400-2*halfHexxy-5)+(10+2*halfHexxy)*i,200+4*(halfHexxy-5), (i+7))
        draw.polygon(verts, fill=color)
    for i in range (0,4):
        verts,color = hexagonMaker(side_length,(400-halfHexxy-5)+(10+2*halfHexxy)*i,200+6*(halfHexxy-5), (i+12))
        draw.polygon(verts, fill=color)
    for i in range (0,3):
        verts,color = hexagonMaker(side_length,400+(10+2*halfHexxy)*i,200+8*(halfHexxy-5), (i+16))
        draw.polygon(verts, fill=color)
    img.save("generated_image.png")


#----------------------------------------------------------------------------------------------------------------------------------------------------------
# main
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    BoardViewer()
    BoardGUI(tiles)

main()