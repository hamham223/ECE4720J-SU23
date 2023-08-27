# Data Preparation

## Goals:
+ Retrieve the data from sftp
+ Read the h5 file and turn into avro

#### Step 1. Mount the dataset from sftp

```bash
echo "password" | sudo -S sshfs /home/hadoopuser/ece472 -o allow_other -o Port=2223 ece472@focs.ji.sjtu.edu.cn: -o IdentityFile=~/.ssh/id_ed25519 1>/dev/null 2>/dev/null
echo "password" | sudo -S mount /home/hadoopuser/ece472/millionsong.iso /home/hadoopuser/ece472/ 1>/dev/null 2>/dev/null
```

#### Step 2.

Use [readh5.py](./readh5.py) to research on the h5 file structure, the details are recorded in [structure](./structure.md)

#### Step 3.

Select useful features and make avro file:

+ features selected are shown in [avsc](./advancedRecommend.avsc)
+ avro files are generated in parallel with pyspark, see [avroSpark.py](./avroSpark.py)

##### Performance

+ With 8 cores processing in parallel, the total time cost to form one `avro` file is reduced from 6 hours to 3 hours.
    
+ The `avro` file generated which is consisted of all desired features of one million songs is approximately `150Mb`.