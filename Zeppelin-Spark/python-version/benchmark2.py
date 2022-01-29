import cmdbench
from cmdbench import benchmark_command, BenchmarkResults
import numpy


def main():
   # command = "python sparkprogram.py"
   command = "python sparkprogram.py --ganres 'Action|Adventure|Animation|Children|Comedy|Crime|Documentary|Drama|Fantasy|Film-Noir|Horror|IMAX|Musical|Mystery|Romance|Sci-Fi|Thriller|War|Western'"
   # command = "python sparkprogram.py --year_from 1990 --year_to 2020 --regexp Y"
   # command = "python sparkprogram.py --N 3 --genres 'Comedy|Action' --year_from 1990 --year_to 2020 --regexp Y"

   benchmark_results = BenchmarkResults()
   for _ in range(100):
     new_benchmark_result = cmdbench.benchmark_command(command)
     benchmark_results.add_benchmark_result(new_benchmark_result)
   print("Average runtime: %s seconds" % benchmark_results.get_averages().process.execution_time)
   avg_memory=benchmark_results.get_averages().memory.max
   print("Average memory: %s MB" % (int(avg_memory)/(1024**2)))
   cpu_arr=benchmark_results.get_averages().time_series.cpu_percentages
   print("Average cpu: %s" % numpy.mean(cpu_arr), '%')


if __name__ == '__main__':
 main()
 