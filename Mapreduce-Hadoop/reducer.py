import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', dest='N', default=25000, type=int,
                        help='The number of top rated movies for each genre. Optional')

    return parser.parse_args()


def shuffle(num_reducers=1):
    shuffled_items = []

    prev_key = None
    values = []

    try:
        for line in sys.stdin:
            key, value = line.split("\t")
            if key != prev_key and prev_key != None:
                shuffled_items.append((prev_key, values))
                values = []
            prev_key = key
            values.append(value)
    except:
        pass
    finally:
        if prev_key != None:
            shuffled_items.append((key, values))

    result = []
    num_items_per_reducer = len(shuffled_items) // num_reducers
    if len(shuffled_items) / num_reducers != num_items_per_reducer:
        num_items_per_reducer += 1
    for i in range(num_reducers):
        result.append(shuffled_items[num_items_per_reducer*i:num_items_per_reducer*(i+1)])

    return result


def reduce(key, values):
    counter = 0
    for value in values:
        if counter < n:
            print(key, value)
            counter += 1


def main():
    pars = get_args()
    global n
    n = int(pars.N)

    for group in shuffle():
        for key, values in group:
            reduce(key, values)


if __name__ == '__main__':
    main()
