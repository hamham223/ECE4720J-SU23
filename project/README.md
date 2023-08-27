# ECE4721J: Project

Big data analysis on [Million Song Dataset (MSD)](http://millionsongdataset.com).

## Goals:

- Work with Hadoop, Drill and Spark
- Compare MapReduce and Spark
- Perform advanced data analysis on big data
- Develop presentations skills (slides + poster)

> Team members: :car:, :hamster:, :crossed_swords: , :palm_tree:

## Part I: Data Preparation

Using the dataset on sftp, we implement

1. Retrieve the dataset, mount using sshfs.
2. Research on the data [structure](./1_preparation/structure.md).
3. Process h5 files and turn into avro in parallel.

For more details, please refer to [preparation](./1_preparation/README.md).

## Part II: Basic Drill Database Query

Based on the `avro` file processed in part I, we

1. Find the range of dates covered by the songs in the dataset, i.e. the age of the oldest and of the youngest songs
2. Find the hottest song that is the shortest and has the highest energy with the lowest tempo.
3. Find the name of the album with the most tracks.
4. Find the name of the band who recorded the longest song. 

The detailed results and codes can be found in [drill queries](./2_drill/README.md).

## Part III: Big Data Recommendation

Use spark mllib and Mapreduce, we implement the following:

1. Find the similar artists of a given song (as input) in parallel
2. Find all the songs of the similar artists in parallel
3. Calculate the distance between the given song and the above song lists in parallel
4. Find the most similar song

More importantly, we can customize the recommendation by changing the weights of the distance function.

For more details, please refer to [recommendation](./3_recommendation/README.md).

## Part IV: Big Data Training and Prediction

Use spark mllib and PCA (dimensional reduction), we implement:

1. Use PCA to reduce the dimension of features from 15 to 6
2. Predict the year of the songs based on PCA features

The source codes are available at [SparkPCA](./4_prediction/sparkpca.py)

## Part V: Final Demonstrations

Use $\LaTeX$, we implement

1. well typed beamer slides
2. A1 Poster showing all our work

For more details, please see [demostration](./5_demostration/)

