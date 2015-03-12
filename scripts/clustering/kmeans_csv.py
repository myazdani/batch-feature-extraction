from sklearn.cluster import KMeans
from pylab import *
import csv
import pickle 

if len(sys.argv) < 2:
    print "Include ANN output file"
    sys.exit()
else:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    num_clusters = int(sys.argv[3])

# In[4]:

def return_rows(filename, file_encoding = 'rU'):
  with open(filename, file_encoding) as f: 
    reader = csv.reader(f)
    rowsInData = [row for row in reader]
  return rowsInData  

# In[5]:

rows = return_rows(in_file)
features = array([row[1:] for row in rows])

# In[18]:

kmeans = KMeans(init='k-means++', n_clusters = num_clusters, n_init=10, n_jobs = -1)

# In[21]:

kmeans.fit(features)

# In[27]:

pickle.dump(kmeans, open(out_file, "wb" ) )