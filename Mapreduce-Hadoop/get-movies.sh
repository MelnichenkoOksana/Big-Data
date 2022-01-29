hdfs dfs -rm /homework/output/*
hdfs dfs -rmdir /homework/output

yarn jar /usr/lib/hadoop/hadoop-streaming.jar
-D mapred.map.tasks=1 \
-D mapred.reduce.tasks=1 \
-input /homework/movies.csv \
-output /homework/output \
-file mapper.py reducer.py \
-mapper "python mapper.py --genres Comedy --year_from 1990 --year_to 2020 --regexp Y" -reducer "python reducer.py --N 3"
