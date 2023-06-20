# ECE4720J Lab 4

> Author: :car::crossed_swords::hamster::palm_tree:

### Ex. 2 — Simple Drill queries

2) Determine the name of the student who had the
a) Lowest grade;
```sqlite
select * from (select columns[0] as name, columns[1] as id, columns[2] as grade from dfs.`D:\drill\5G_file.csv`) where grade = (select min(grade) from (select columns[0] as name, columns[1] as id, columns[2] as grade from dfs.`D:\drill\5G_file.csv`));
```
The result is too long to be put here.

b) Highest average score;
```sqlite
select * from(select name, avg(cast(grade as int)) as avgscore from (select columns[0] as name, columns[1] as id, columns[2] as grade from dfs.`D:\drill\5G_file.csv`) group by name) where avgscore = (select max(avgscore) from (select name, avg(cast(grade as int)) as avgscore from (select columns[0] as name, columns[1] as id, columns[2] as grade from dfs.`D:\drill\5G_file.csv`) group by name));
```
```
+-------------------+----------+
|       name        | avgscore |
+-------------------+----------+
| Ronny Kreger      | 100.0    |
| Ardell Jubeh      | 100.0    |
| Marx Dobrich      | 100.0    |
| Bennie Donaher    | 100.0    |
| Carmelia Riglos   | 100.0    |
| Allison Mccullors | 100.0    |
| Doria Rener       | 100.0    |
| Miranda Redfern   | 100.0    |
| Chanda Scholtz    | 100.0    |
| Janae Nagle       | 100.0    |
| Dorotha Tointon   | 100.0    |
+-------------------+----------+
11 rows selected (222.824 seconds)

```
3) Calculate the median over all the scores.
```sqlite
select (cast(grade as int)) as median from ( select grade, ROW_NUMBER() over (order by grade) as row_num, count(*) over () as total_rows from (select columns[0] as name, columns[1] as id, columns[2] as grade from dfs.`D:\drill\5G_file.csv`)) sub where row_num in (floor((total_rows+1)/2), ceil((total_rows+1)/2));
```
```
+--------+
| median |
+--------+
| 53     |
+--------+
1 row selected (112.286 seconds)

```

### Ex. 3 Simple Spark

+ pyspark `map` `reduce` example:

```python
from pyspark.context import SparkContext

sc = SparkContext()
name = "./small_file.csv"
textFile = sc.textFile(name)
grades = textFile.flatMap(lambda x: [x.split(",")[0], int(x.split(",")[1])])
grades = textFile.map(lambda x: (x.split(",")[0], int(x.split(",")[1])))
maxGrade = grades.reduceByKey(lambda a, b:max(a,b))
maxGrade.saveAsTextFile()
```

+ `spark-submit` command

```bash
spark-submit \
--master yarn \
--deploy-mode cluster \
--conf spark.pyspark.driver.python=python3 \
--conf spark.pyspark.python=python3 \
ex3.py -n <size>
```

`<size> ` can be `10k`, `20k`,`50k`,`100k`,...

