
# coding: utf-8

# In[1]:

import os
import csv
import cv2
from pylab import *
from PIL import Image
from skimage.feature import hog
#from joblib import Parallel, delayed
import numpy as np


if len(sys.argv) < 2:
    print "Include ANN output file"
    sys.exit()
else:
    in_file = sys.argv[1]
    out_file = sys.argv[2]

# In[2]:

src_path, image_type = in_file, ".jpg"
image_paths = []
for root, dirs, files in os.walk(src_path):
    image_paths.extend([os.path.join(root, f) for f in files if f.endswith(image_type)])


# In[3]:

def grayscale_return(im_path):
    # read image
    im = cv2.imread(im_path)
    if str(type(im)) == "<type 'NoneType'>":
        return None
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(im, (75, 75)) 
    return resized_image.reshape((1,75*75)).flatten()


# In[4]:

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


# In[5]:

chunk_size = 10
print "number of images is", len(image_paths)
image_paths_chunks = list(chunks(image_paths, chunk_size))
print "number of chunks is", len(image_paths_chunks)


# In[6]:

def get_gray_chunks(image_paths_chunk):
    return [[image_path, grayscale_return(image_path)] for image_path in image_paths_chunk]


# In[7]:

csvfile = open(out_file, "a")
resultswrtier = csv.writer(csvfile, delimiter = ",")


# In[8]:

def write_to_file(res):
    for r in res:
        try:
            row = [r[0]]
            temp = [float(val) for val in r[1]]
            row.extend(temp)
            resultswrtier.writerow(row)
        except:
            print r[0],"failed" 


# In[9]:

for i, image_paths_chunk in enumerate(image_paths_chunks):
    print "chunk", i
    result = get_gray_chunks(image_paths_chunk)
    write_to_file(result)

csvfile.close()

