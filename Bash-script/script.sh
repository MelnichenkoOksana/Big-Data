hdfs dfs -mkdir /homework
wget https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
unzip ml-latest-small.zip
hdfs dfs -put ml-latest-small /homework/
hdfs dfs -cat /homework/ml-latest-small/movies.csv | head -n 10
hdfs dfs -cat /homework/ml-latest-small/ratings.csv | head -n 10
hdfs dfs -du /homework/ml-latest-small
hdfs dfs -touchz /homework/Hello.txt
rm -r /home/melnicenkooksana1990/ml-latest-small
rm -r /home/melnicenkooksana1990/ml-latest-small.zip