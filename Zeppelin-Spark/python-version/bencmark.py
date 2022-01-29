import cmdbench
from cmdbench import benchmark_command, BenchmarkResults

def main():
    benchmark_results = BenchmarkResults()
    for _ in range(100):
        new_benchmark_result = cmdbench.benchmark_command("python sparkprogram.py --N 3 --genres 'Comedy|Action' --year_from 1990 --year_to 2020 --regexp Y")
        #new_benchmark_result = cmdbench.benchmark_command("python sparkprogram.py -year_from 1990 -year_to 2020 -regexp Y")
        # new_benchmark_result = cmdbench.benchmark_command("python sparkprogram.py")
        benchmark_results.add_benchmark_result(new_benchmark_result)
    print(benchmark_results.get_averages())


if __name__ == '__main__':
    main()