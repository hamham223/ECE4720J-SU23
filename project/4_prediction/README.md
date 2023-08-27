# Big Data Prediction

### Part I: Dimensional Reduction

```python
def getPCA():
    spark_df = spark.read.options(header='true', inferSchema='true').csv('file:///home/hadoopuser/project/predict/data2/trn.csv')
    spark_df = spark_df.fillna(0).drop('_c0')

    feature_cols = spark_df.drop('coarse_classified_class_year').columns
    feature_assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')
    feature_df = feature_assembler.transform(spark_df).select('coarse_classified_class_year','features')

    pca = PCA(k=7, inputCol='features', outputCol='pca_features')
    pca_model = pca.fit(feature_df)
    return pca_model
```

### Part II: Big Data Prediction

We treat it as a classification problem

```python
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
lrm = LogisticRegressionWithLBFGS.train(sc.parallelize(data_train, 200), iterations=200, numClasses=18)
```