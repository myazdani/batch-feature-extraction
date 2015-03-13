from sklearn.cluster import KMeans
from pylab import *
import csv
import pickle 

if len(sys.argv) < 2:
    print "Enter 3 arguments for featue file, cluster file, and out file"
    sys.exit()
else:
    feature_file = sys.argv[1]
    cluster_file = sys.argv[2]
    out_file = sys.argv[3]


def return_rows(filename, file_encoding = 'rU'):
  with open(filename, file_encoding) as f: 
    reader = csv.reader(f)
    rowsInData = [row for row in reader]
  return rowsInData  

# In[5]:

rows = return_rows(feature_file)
features = array([map(float, row[1:]) for row in rows])

kmeans = pickle.load(open(cluster_file, "rb"))

cluster_dists = kmeans.transform(features)

clusters = []
for i, row in enumerate(rows):
    min_cluster = argmin(cluster_dists[i])
    clusters.append([row[0], min_cluster, cluster_dists[i][min_cluster]])

csvfile = open(out_file, "wb")
writerows = csv.writer(csvfile, delimiter = ",")
for cluster in clusters:
    writerows.writerow(cluster)
csvfile.close()