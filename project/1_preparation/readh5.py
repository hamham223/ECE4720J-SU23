#necessary library to read a h5 file
import h5py
#read a file with h5py
file = h5py.File('/home/hadoopuser/ece472/data/A/X/L/TRAXLZU12903D05F94.h5', 'r')

#extract the keys in the first level
groups = list(file.keys())
print(groups) #['analysis', 'metadata', 'musicbrainz']

#extract the keys in the second level
group = file[groups[0]]
datasets = list(group.keys())
print(datasets)

#extract the data
dataset = group[datasets[-3]]
#Retrieve the data as a NumPy array
data = dataset[()]
print(data)
