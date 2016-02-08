from __future__ import division
## modified by liu liu
## leoliu@u.northwestern.edu

## Kyle Dickerson
## kyle.dickerson@gmail.com
## Jan 15, 2008
##
## Self-organizing map using scipy
## This code is licensed and released under the GNU GPL

## This code uses a square grid rather than hexagonal grid, as scipy allows for fast square grid computation.
## I designed sompy for speed, so attempting to read the code may not be very intuitive.
## If you're trying to learn how SOMs work, I would suggest starting with Paras Chopras SOMPython code:
##  http://www.paraschopra.com/sourcecode/SOM/index.php
## It has a more intuitive structure for those unfamiliar with scipy, however it is much slower.

## If you do use this code for something, please let me know, I'd like to know if has been useful to anyone.

from random import *
from math import *
import sys
import scipy
import traceback
class SOM:

    def __init__(self, height=10, width=10, FV_size=10, learning_rate=0.005):
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.radius = (height+width)/3
        self.learning_rate = learning_rate
        self.nodes = scipy.array([[ [random() for i in range(FV_size)] for x in range(width)] for y in range(height)])
    
    # train_vector: [ FV0, FV1, FV2, ...] -> [ [...], [...], [...], ...]
    # train vector may be a list, will be converted to a list of scipy arrays
    def train(self, iterations=1000, train_vector=[[]]):
        for t in range(len(train_vector)):
            train_vector[t] = scipy.array(train_vector[t])
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0.0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        
        for i in range(1, iterations+1):
            delta_nodes.fill(0)
            radius_decaying=self.radius*exp(-1.0*i/time_constant)
            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying=self.learning_rate*exp(-1.0*i/time_constant)
            sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations))
            
            for j in range(len(train_vector)):
                best = self.best_match(train_vector[j])
                for loc in self.find_neighborhood(best, radius_decaying):
                    influence = exp( (-1.0 * (loc[2]**2)) / rad_div_val)
                    inf_lrd = influence*learning_rate_decaying
                    
                    delta_nodes[loc[0],loc[1]] += inf_lrd*(train_vector[j]-self.nodes[loc[0],loc[1]])
            self.nodes += delta_nodes
        sys.stdout.write("\n")
    
    # Returns a list of points which live within 'dist' of 'pt'
    # Uses the Chessboard distance
    # pt is (row, column)
    def find_neighborhood(self, pt, dist):
        min_y = max(int(pt[0] - dist), 0)
        max_y = min(int(pt[0] + dist), self.height)
        min_x = max(int(pt[1] - dist), 0)
        max_x = min(int(pt[1] + dist), self.width)
        neighbors = []
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                dist = abs(y-pt[0]) + abs(x-pt[1])
                neighbors.append((y,x,dist))
        return neighbors
    
    # Returns location of best match, uses Euclidean distance
    # target_FV is a scipy array
    # modified for more than 3 dimensions: liu
    def best_match(self, target_FV):
        loc = scipy.argmin((((self.nodes - target_FV)**2).sum(axis=2))**0.5)
        r = 0
        while loc > self.width:
            loc -= self.width
            r += 1
        c = loc
        return (r, c)

    # returns the Euclidean distance between two Feature Vectors
    # FV_1, FV_2 are scipy arrays
    def FV_distance(self, FV_1, FV_2):
        return (sum((FV_1 - FV_2)**2))**0.5

def main(colors=None,width=None,height=None,labels=None,num_iter=None,learn_rate=None):
    print "Initialization..."
    if colors is None:
        colors = [ [0, 0, 0,1], [0, 0, 255,2], [0, 255, 0,3], [0, 255, 255,4], [255, 0, 0,5], [255, 0, 255,6], [255, 255, 0,7], [255, 255, 255,8]]
    if width is None:
        width = 40
    if height is None:
        height = 40
    if labels is None:
        labels = ['0','1','2','3','4','5','6','7']
    if num_iter is None:
        num_iter = 1000
    if learn_rate is None:
        learn_rate = 0.05
    color_som = SOM(width,height,len(colors[0]),learn_rate)
    print "Training colors..."
    color_som.train(num_iter, colors)
    try:
        from PIL import Image,ImageDraw,ImageFont
        print "Saving Image: sompy_test_colors.png..."
        img = Image.new("RGB", (width, height))
        font = ImageFont.truetype("/Library/Fonts/Times New Roman.ttf", 9)
        for r in range(height):
            for c in range(width):
                img.putpixel((c,r),(255,255,255))
                #img.putpixel((c,r), (int(color_som.nodes[r,c,0]), int(color_som.nodes[r,c,1]), int(color_som.nodes[r,c,2])))
        draw = ImageDraw.Draw(img)
        for i in xrange(len(labels)):
            loc = color_som.best_match(colors[i])
            if labels[i] == 'A':
                color = (255,0,0)
            else:
                color = (51,153,255)
            draw.text((max(loc[1]-3,3),max(loc[0]-3,3)),labels[i],color,font = font)
        #draw.text((0, 0),"Sample Text",(0,0,0))
        #img = img.resize((width*30, height*30),Image.BICUBIC)
        img.save("sompy_test_colors.png")
    except Exception,e:
        traceback.print_exc()
        print str(e),"Error saving the image, do you have PIL (Python Imaging Library) installed?"
if __name__ == '__main__':
    main()
