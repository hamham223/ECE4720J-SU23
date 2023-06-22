from pyspark.context import SparkContext
from argparse import ArgumentParser

def parse_args(description):
    parser = ArgumentParser(description=description)
    parser.add_argument("-n", type=str, default="50k",
                        required=True, help="The filename")
    args = parser.parse_args()
    return args

args = parse_args("VE472 Lab4")
filename = args.n
sc = SparkContext()
name = "hdfs://hadoop-master:9000/records_"+filename+".csv"
textFile = sc.textFile(name)
#grades = textFile.flatMap(lambda x: [x.split(",")[0], int(x.split(",")[1])])
grades = textFile.map(lambda x: (x.split(",")[0], int(x.split(",")[2])))
maxGrade = grades.reduceByKey(lambda a,b:max(a,b))
maxGrade.saveAsTextFile("hdfs://hadoop-master:9000/lab4_"+filename)
