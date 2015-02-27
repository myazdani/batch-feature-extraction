import os
from PIL import Image, ImageDraw
from numpy import *
from pylab import *
import pickle
import csv
import pca
from scipy.cluster.vq import *


featuresFilename = "/Users/myazdaniUCSD/Documents/batch_feature_extraction/hue_sample.csv"
outfile = "PCA.png"

with open(featuresFilename, 'rU') as f:
  reader = csv.reader(f)
  all_rows = [row for row in reader]

rows = all_rows[170:-100]
feature_matrix = []
image_paths = []

for row in rows:
  image_paths.append(row[0])
  features = [float(r) for r in row[1:]]
  feature_matrix.append(features)

feature_matrix = array(feature_matrix)

V,S,immean = pca.pca(feature_matrix)
projected_features = array([dot(V[[1,2]],feature_matrix[i]-immean) for i in range(len(image_paths))])

h,w = 20000,20000
img = Image.new('RGB',(w,h),(255,255,255))
draw = ImageDraw.Draw(img)

scale = abs(projected_features).max(0)
scaled = floor(array([ (p / scale) * (w/2-20,h/2-20) + (w/2,h/2) for p in projected_features]))
print "number of images", len(image_paths)
for i in range(len(image_paths)):
  nodeim = Image.open(image_paths[i]) 
  nodeim = nodeim.resize((275,275))
  ns = nodeim.size 
  img.paste(nodeim,(int(scaled[i][0]-ns[0]//2),int(scaled[i][1]-ns[1]//2),int(scaled[i][0]+ns[0]//2+1),int(scaled[i][1]+ns[1]//2+1))) 

img.save(outfile)