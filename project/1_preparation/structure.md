# H5 Data Structure

**Reference http://millionsongdataset.com/pages/example-track-description/**

This issue is intended to help you get familiar with the structure of a h5 file so as to aid you with further analysis.

Each h5 file is a single song with its information (but not the song itself). Here is a python code that extracts a h5 file:
```python
#necessary library to read a h5 file
import h5py
#read a file with h5py
file = h5py.File('/media/zjche/million song dataset/data/A/X/L/TRAXLZU12903D05F94.h5', 'r')

#extract the keys in the first level
groups = list(file.keys())
print(groups) #['analysis', 'metadata', 'musicbrainz']

#extract the keys in the second level
group = file[groups[0]]
datasets = list(group.keys())
print(datasets)

#extract the data
dataset = group[datasets[0]]
#Retrieve the data as a NumPy array
data = dataset[()]
print(data)
```
As you can see, a h5 file contains data of 3 levels. Here I will try my best to list every single piece in a h5 file with the example of `TRAXLZU12903D05F94.h5`.
## File name
In `TRAXLZU12903D05F94.h5`, "TR" indicates that the file is a **song**, "AXL" indicates that it is in the folder `.../A/X/L/`

## Structure

| Key level 1 | Key level 2 				| Description | Data |
| -------- 	  | -------- 					| -------- |--------|
| analysis    | bars_confidence     		| Confidence value (between 0 and 1) associated with each bar by The Echo Nest. |	|
| 		      | bars_start		     		| Start time of each bar according to The Echo Nest, this song has 99 bars.     |	|
| 		      | beats_confidence		    | Confidence value (between 0 and 1) associated with each beat by The Echo Nest.     |	|
| 		      | beats_start		     		| Start time of each beat according to The Echo Nest, this song has 397 beats.     |	|
| 		      | sections_confidence	    	| Confidence value (between 0 and 1) associated with each section by The Echo Nest.     |	|
| 		      | sections_start		     	| Start time of each section according to The Echo Nest, this song has 10 sections.     |	|
| 		      | segments_confidence	    	| Confidence value (between 0 and 1) associated with each segment by The Echo Nest.     |	|
| 		      | segments_loudness_max	    | Max loudness during each segment.     |	|
| 		      | segments_loudness_max_time  | Time of the max loudness during each segment.     |	|
| 		      | segments_loudness_start		| Loudness at the beginning of each segment.     |	|
| 		      | segments_pitches		    | Chroma features for each segment (normalized so max is 1.)     |	|
| 		      | segments_start		     	| Start time of each segment (~ musical event, or onset) according to The Echo Nest, this song has 935 segments.     |	|
| 		      | segments_timbre		    	| MFCC-like features for each segment .    |	|
| 		      | songs		     			| (?, ?, danceability, duration(seconds), end_of_fade_in, energy, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, key_confidence, loudness, mode, mode_confidence, start_of_fade_out, tempo, time_signature, time_signature_confidence, track_id)     |	|
| 		      | tatums_confidence		    | Confidence value (between 0 and 1) associated with each tatum by The Echo Nest.     |	|
| 		      | tatums_start		     	| Start time of each tatum according to The Echo Nest, this song has 794 tatums.     |	|
| metadata    | artist_terms				| This artist has 12 terms (tags) from The Echo Nest.    | [b'dance pop' b'rock' b'pop' b'england' b'adult contemporary' b'ballad' b'club' b'classic' b'male' b'cover' b'soul' b'80s']	|
|  			  | artist_terms_freq		    | Frequency of the 12 terms from The Echo Nest (number between 0 and 1).     | [1.         1.         0.91010297 0.66295815 0.56316029 0.53233546 0.49859374 0.24929687 0.19954646 0.05768186 0.25335706 0.        ]	|
|  			  | artist_terms_weight	    	| Weight of the 12 terms from The Echo Nest (number between 0 and 1).     |	[1.         0.75590423 0.72334284 0.72294536 0.68418867 0.64847932 0.57580382 0.38442392 0.35655972 0.31875528 0.31759202 0.13391383]|
|  			  | similar_artists		    	| IDs of similar artists     | [b'ARCJMMQ1187B98D1FD' b'ARY7CAU1187B98A4F6' b'ARIJPXL1187B9AB43A' b'ARYAUMZ1187B9A2A40' ...]	|
|  			  | songs					    | (?, ?, ?, ?, artist_id, ?, ?, ?, artist_mbid, artist_name, artist_playmeid, ?, ?, ?, album_name, album_id, song_hotttnesss, song_id, song_title, track_7digitalid)     |	|
| musicbrainz | artist_mbtags				| Tags descripting the artist who wrote this song in a list.     | [b'uk' b'british' b'english' b'classic pop and rock']	|
|			  | artist_mbtags_count			| Raw tag count of the tags this artist received.      | [1 1 1 1]	|
|			  | songs				 		| A tuple consisting of 0 and the year when the song published. Might be (0,0) if data missing.      | (0,1987)	|

