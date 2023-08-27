from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler,PCA
from pyspark.sql import Row, SQLContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithSGD, LogisticRegressionWithLBFGS, LogisticRegressionModel
import pandas as pd
spark = SparkSession.builder.master("local[8]") \
                            .appName("PCA") \
                            .config("spark.executor.memory", "6g") \
                            .config("spark.executor.cores", "8") \
                            .getOrCreate()
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

def df2label(record: Row) -> LabeledPoint:
    rec = list(record)
    return LabeledPoint(float(rec[0])-1, rec[1:])

def getPCA():
    spark_df = spark.read.options(header='true', inferSchema='true').csv('file:///home/hadoopuser/project/predict/data2/trn.csv')
    spark_df = spark_df.fillna(0).drop('_c0')

    feature_cols = spark_df.drop('coarse_classified_class_year').columns
    feature_assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')
    feature_df = feature_assembler.transform(spark_df).select('coarse_classified_class_year','features')

    pca = PCA(k=7, inputCol='features', outputCol='pca_features')
    pca_model = pca.fit(feature_df)
    return pca_model


def train(pca_model):
    spark_df = spark.read.options(header='true', inferSchema='true').csv('file:///home/hadoopuser/project/predict/data2/trn.csv')
    spark_df = spark_df.fillna(0).drop('_c0')

    feature_cols = spark_df.drop('coarse_classified_class_year').columns
    feature_assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')
    feature_df = feature_assembler.transform(spark_df).select('coarse_classified_class_year','features')

    pca_df = pca_model.transform(feature_df)
    res_df = pca_df.select('coarse_classified_class_year','pca_features').rdd.map(lambda x: Row(
                                                             tag=x[0],
                                                             PC1=float(x[1][0]), 
                                                             PC2=float(x[1][1]),
                                                             PC3=float(x[1][2]),
                                                             PC4=float(x[1][3]),
                                                             PC5=float(x[1][4]),
                                                             PC6=float(x[1][5]))).toDF()
    data = res_df.collect()
    data_train = sc.parallelize(data,100).map(df2label).collect()

    lrm = LogisticRegressionWithLBFGS.train(sc.parallelize(data_train, 200), iterations=200, numClasses=18)
    print("Weights:", lrm.weights)
    lrm.save(sc,'file:///home/hadoopuser/project/predict/model')

def test(pca_model):
    val_df = spark.read.options(header='true', inferSchema='true').csv('file:///home/hadoopuser/project/predict/data2/val_x.csv')
    val_df = val_df.fillna(0).drop('_c0')

    feature_cols = val_df.drop('coarse_classified_class_year').columns
    feature_assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')
    val_feature_df = feature_assembler.transform(val_df).select('features')

    pca_val_df = pca_model.transform(val_feature_df)
    res_val_df = pca_val_df.select('pca_features').rdd.map(lambda x: Row(
                                                                PC1=float(x[0][0]), 
                                                                PC2=float(x[0][1]),
                                                                PC3=float(x[0][2]),
                                                                PC4=float(x[0][3]),
                                                                PC5=float(x[0][4]),
                                                                PC6=float(x[0][5]))).toDF()

    lrm = LogisticRegressionModel.load(sc,'file:///home/hadoopuser/project/predict/model')
    res_dat = res_val_df.collect()
    res = []
    for r in res_dat:
        print(r)
        row = list(r)
        y = lrm.predict(row[:])
        res.append(int(y+1))
    pd.DataFrame(res,columns=['year_predict']).to_csv("./data2/prd_y.csv")

if __name__ == "__main__":
    test(getPCA())
sc.stop()