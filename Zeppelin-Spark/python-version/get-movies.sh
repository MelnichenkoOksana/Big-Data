if hdfs dfs -test -d /result; then
 hdfs dfs -rm -r /result
 
fi


while [ -n "$1" ]
do
case "$1" in
  --regexp)
  regexp=$1
  regexp_v=$2
;;
  --year_from)
  year_from=$1
  year_from_v=$2
;;
  --year_to)
  year_to=$1
  year_to_v=$2
;;
  --genres)
  genres=$1
  genres_v=$2
;;
  --N)
  N=$1
  N_v=$2
;;
esac
shift
done


python sparkprogram.py $regexp $regexp_v $year_from $year_from_v $year_to $year_to_v $genres $genres_v $N $N_v
hdfs dfs -cat /result/*