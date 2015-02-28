
# coding: utf-8

# In[1]:

import os
import cv2
import csv
from pylab import *
import scipy
import scipy.misc
from PIL import Image
from skimage.util.shape import view_as_blocks, view_as_windows
#from joblib import Parallel, delayed
import numpy as np
from scipy import stats
import cPickle as pickle
import sys

# In[2]:

if len(sys.argv) < 2:
    print "Include input path and output file name (with .csv extenstion)"
    sys.exit()
else:
    in_path = sys.argv[1]
    out_file = sys.argv[2]


src_path, image_type = in_path, ".jpg"
image_paths = []
for root, dirs, files in os.walk(src_path):
    image_paths.extend([os.path.join(root, f) for f in files if f.endswith(image_type)])


# In[ ]:

num_zones = 1 # 1 = entire images
channel = 0 # 0 = Hue, 1 = Saturation, 2 = Value


# In[3]:

def HSVhist_cv(im_path, num_blocks, channels = range(3)):
    # read image
    im = cv2.imread(im_path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    if str(type(im)) == "<type 'NoneType'>":
        return None
    # set block step sizes
    step_x = im.shape[0]/num_blocks
    step_y = im.shape[1]/num_blocks
    hists = {}
    for i in range(num_blocks):
            for j in range(num_blocks):
                # set starting and ending indices for row blocks
                if i < (num_blocks-1): 
                    start_x, end_x = i*step_x, (i+1)*step_x
                # deal with the edge case row blocks
                else:
                    start_x, end_x = i*step_x, im.shape[0]
                # set starting and ending indices for vertical blocks
                if j < (num_blocks-1):
                    start_y, end_y = j*step_y, (j+1)*step_y
                # deal with the edge case vertical blocks
                else:
                    start_y, end_y = j*step_y, im.shape[1]    
                #copy image into block
                im_block = im[start_x:end_x, start_y:end_y,:].copy()
                hist_channels = []
                if type(channels) == int:
                    if channels == 0:
                        hist_temp = cv2.calcHist([im_block],[channels],None,[180],[0,180])
                        hist_channels.append(hist_temp/(max(hist_temp)+1.0))
                    else:
                        hist_temp = cv2.calcHist([im_block],[channels],None,[256],[0,256])
                        hist_channels.append(hist_temp/(max(hist_temp)+1.0))   
                else:                   
                    for channel in channels: 
                        if channel == 0:
                            hist_temp = cv2.calcHist([im_block],[channel],None,[180],[0,180])
                            hist_channels.append(hist_temp/(max(hist_temp)+1.0))
                        else:
                            hist_temp = cv2.calcHist([im_block],[channel],None,[256],[0,256])
                            hist_channels.append(hist_temp/(max(hist_temp)+1.0))
                hists[(start_x, end_x, start_y, end_y)] = hist_channels
    return hists

def HSVhist_pretty(image_path, num_zones = 1, channels = range(3)):
    hists = HSVhist_cv(image_path, num_zones, channels)
    features = []
    for key in sorted(hists.keys()):
        l = hists[key]
        ## flatten list of lists (list of histogram lists)
        features.append([item for sublist in l for item in sublist])
    return [item for sublist in features for item in sublist]


# In[4]:

def HUEhist_cv(im_path, num_blocks):
    # read image
    im = cv2.imread(im_path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    if str(type(im)) == "<type 'NoneType'>":
        return None
    # set block step sizes
    step_x = im.shape[0]/num_blocks
    step_y = im.shape[1]/num_blocks
    hists = {}
    for i in range(num_blocks):
            for j in range(num_blocks):
                # set starting and ending indices for row blocks
                if i < (num_blocks-1): 
                    start_x, end_x = i*step_x, (i+1)*step_x
                # deal with the edge case row blocks
                else:
                    start_x, end_x = i*step_x, im.shape[0]
                # set starting and ending indices for vertical blocks
                if j < (num_blocks-1):
                    start_y, end_y = j*step_y, (j+1)*step_y
                # deal with the edge case vertical blocks
                else:
                    start_y, end_y = j*step_y, im.shape[1]    
                #copy image into block
                im_block = im[start_x:end_x, start_y:end_y,:].copy()
                hue_hist = cv2.calcHist([im_block],[0],None,[180],[0,180])
                hists[(start_x, end_x, start_y, end_y)] = hue_hist
    return hists

def HUEhist_pretty(image_path, num_zones = 1):
    hists = HUEhist_cv(image_path, num_zones)
    features = []
    for key in sorted(hists.keys()):
        l = hists[key]
        ## flatten list of lists (list of histogram lists)
        features.append([item for sublist in l for item in sublist])
    return [item for sublist in features for item in sublist]


# In[5]:

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


# In[6]:

chunk_size = 50
print "number of images is", len(image_paths)
image_paths_chunks = list(chunks(image_paths, chunk_size))
print "number of chunks is", len(image_paths_chunks)


# In[7]:

def get_HSV_hist_chunks(image_paths_chunk):
    return [[image_path, HSVhist_pretty(image_path, num_zones, channel)] for image_path in image_paths_chunk]


# In[8]:

csvfile = open(out_file, "a")
resultswrtier = csv.writer(csvfile, delimiter = ",")


# In[9]:

def write_to_file(res):
    for r in res:
        try:
            row = [r[0]]
            temp = [float(hist_val) for hist_val in r[1]]
            row.extend(temp)
            resultswrtier.writerow(row)
        except:
            print r[0],"failed" 


# In[10]:

for i, image_paths_chunk in enumerate(image_paths_chunks):
    print "chunk", i
    result = get_HSV_hist_chunks(image_paths_chunk)
    write_to_file(result)

csvfile.close()


