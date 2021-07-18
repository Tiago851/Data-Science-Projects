'''

This project was based on the project idea from (https://data-flair.training/blogs/project-in-python-colour-detection/)
and serves as an introduction to OpenCV and its modules.

A more basic script for blurring an image using OpenCV can be found on my Github.

'''

#Libraries
import cv2
import numpy as np
import pandas as pd
import argparse

#argparse library to create an argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Reading image with opencv
img = cv2.imread(img_path)

#Declaring global variable
clicked = False
r = g = b = xpos = ypos = 0

#Opening the file
index = ['Color', 'Color Name', 'Hex', 'R', 'G', 'B']
df = pd.read_csv('C:\\Users\\Utilizador\\Desktop\\Data Science\\colors.csv', names = index, header = None)

#Setting draw_function
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#Calculate distance to get color name
def calculate_d(R,G,B):
    minimum = 10000
    for i in range(len(df)):
        d = abs(R - df.loc[i, 'R'])+ abs(G - df.loc[i, 'G']) + abs(B - df.loc[i, 'B'])
        
        if (d <= minimum):
            minimum = d
            cname = df.loc[i, 'Color Name']
    
    return cname

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

"""
Whenever a double click event occurs, it will update the color name and RGB values on the window.
Using the cv2.imshow() function, we draw the image on the window. 
When the user double clicks the window, we draw a rectangle and get the color name to draw text on the window 
using cv2.rectangle and cv2.putText() functions.
"""
while (1):
    cv2.imshow('image', img)

    if clicked:
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)
        cv2.rectangle(img, (20,20), (750,60), (b,g,r), -1)

        #Creating text string to display ( Color name and RGB values)
        texto = calculate_d(r,g,b) + ' R = ' + str(r) + ' G = ' + str(g) + ' B = ' + str(b)

        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool))
        cv2.putText(img, texto, (50,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)
        
        #For very light colours we will display text in black colour
        if (r+g+b >= 600):
            cv2.putText(img, texto, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

        clicked = False

    #Break the loop when the user presses 'esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()