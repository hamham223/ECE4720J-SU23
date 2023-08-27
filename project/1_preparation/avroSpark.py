import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import os
import h5py
from typing import Literal, List
import threading
import fastavro
from loguru import logger

from pyspark import SparkContext
sc = SparkContext()
folder_path = r'/home/hadoopuser/ece472/data'
data = [chr(character+ord('A')) for character in range(26)]
schema = avro.schema.parse(open("advancedRecommend.avsc", "rb").read())

def traverse_folder(folder_path: str,writer: DataFileWriter):
    for item in os.listdir(folder_path):
        
        file_path = os.path.join(folder_path, item)
        if os.path.isfile(file_path):
            #print("Reading File: " + str(file_path))
            file = h5py.File(file_path, 'r')

            bar_num = float(len(file['analysis']['bars_start'][()]))
            beat_num = float(len(file['analysis']['beats_start'][()]))
            section_num = float(len(file['analysis']['sections_start'][()]))
            segment_num = float(len(file['analysis']['segments_start'][()]))

            danceability = float(list(file['analysis']['songs'][()])[0][2])
            duration = float(list(file['analysis']['songs'][()])[0][3])
            end_of_fade_in = float(list(file['analysis']['songs'][()])[0][4])
            energy = float(list(file['analysis']['songs'][()])[0][5])
            loudness = float(list(file['analysis']['songs'][()])[0][-8])
            mode = float(list(file['analysis']['songs'][()])[0][-7])
            start_of_fade_out = float(list(file['analysis']['songs'][()])[0][-5])
            tempo = float(list(file['analysis']['songs'][()])[0][-4])
            time_signature = float(list(file['analysis']['songs'][()])[0][-3])
            track_id = list(file['analysis']['songs'][()])[0][-1]
            tatum_num = float(len(file['analysis']['tatums_start'][()]))

            artist_id = list(file['metadata']['songs'][()])[0][4]
            artist_name = list(file['metadata']['songs'][()])[0][9]
            hotness = float(list(file['metadata']['songs'][()])[0][-4])
            song_id = list(file['metadata']['songs'][()])[0][-3] # string
            title = list(file['metadata']['songs'][()])[0][-2]

            album_id = int(list(file['metadata']['songs'][()])[0][-5]) # int
            year = float(list(file['musicbrainz']['songs'][()])[0][1])
            
            writer.append({"bar_num":bar_num,
                           "beat_num":beat_num,
                           "section_num":section_num,
                           "segment_num":segment_num,
                           
                           "danceability":danceability,
                           "duration":duration,
                           "end_of_fade_in":end_of_fade_in,
                           "energy":energy,
                           "loudness":loudness,
                           "mode":mode,
                           "start_of_fade_out":start_of_fade_out,
                           "tempo":tempo,
                           "time_signature":time_signature,
                           "track_id":track_id,
                           "tatum_num":tatum_num,
                           
                           "artist_id":artist_id,
                           "artist_name":artist_name,
                           "hotness":hotness,
                           "song_id":song_id,
                           "title":title,
                           
                           "album_id":album_id,
                           "year":year})
            file.close()
        else:
            print("In folder: "+ str(file_path))
            traverse_folder(file_path,writer)
def avro_with_one_letter(c: Literal['A']):
    writer = DataFileWriter(open("./avro_files/songs_"+str(c)+".avro", "wb"), DatumWriter(), schema)
    traverse_folder(folder_path+"/"+str(c),writer)
    writer.close()
    pass

if __name__ == "__main__":
    try:
        result_rdd = sc.parallelize(data,26).map(avro_with_one_letter)
        result_rdd.collect()
        
        merged_results = None
        merged_schema = None
        for i in range(0,26):
            with open("avro_files/songs_"+str(chr(ord('A')+i))+".avro","rb") as f:
                reader = fastavro.reader(f)
                records = [record for record in reader]
                if merged_results == None:
                    merged_results = records
                    merged_schema = reader.writer_schema
                else:
                    merged_results = merged_results + records

            with open("songs_advanced.avro",'wb') as f:
                fastavro.writer(f,merged_schema,merged_results)
    except Exception as error:
        logger.exception(error)
#result = result_rdd.collect()
#print(result)
