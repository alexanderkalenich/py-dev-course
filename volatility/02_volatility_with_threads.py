# -*- coding: utf-8 -*-

import glob
import os
import threading
import time
from collections import defaultdict


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result

    return surrogate


class Volatility(threading.Thread):

    def __init__(self, csvfile, lock, id_list, id_list_zero, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csvfile = csvfile
        self.min_max_lock = lock
        self.secid_list = id_list
        self.secid_list_zero = id_list_zero

    def run(self):
        with open(self.csvfile, 'r', encoding='utf8') as ff:
            maximum = 0
            minimum = 0
            for line in ff:
                line = line.rstrip()
                secid, tradetime, price, quantity = line.split(',')
                if not price.isalpha():
                    price = float(price)
                    if minimum > 0:
                        if price > maximum:
                            maximum = price
                        elif price < minimum:
                            minimum = price
                    else:
                        minimum = maximum = price
            minimum = round(minimum, 2)
            maximum = round(maximum, 2)
            half_sum = (maximum + minimum) / 2
            volatility_value = ((maximum - minimum) / half_sum) * 100
            with self.min_max_lock:
                if volatility_value == 0:
                    self.secid_list_zero[secid] = round(volatility_value, 2)
                else:
                    self.secid_list[secid] = round(volatility_value, 2)


class Processing:

    def __init__(self, gl_secid_list, gl_secid_list_zero):
        self.secid_list = gl_secid_list
        self.secid_list_zero = gl_secid_list_zero

    def file_processing(self):
        print(f'Максимальная волатильность:')
        for ticker, vol in sorted(self.secid_list.items(), key=lambda pair: pair[1], reverse=True)[:3]:
            print(f'{ticker} - {vol} %')
        print(f'Минимальная волатильность:')
        for ticker, vol in sorted(self.secid_list.items(), key=lambda pair: pair[1], reverse=True)[-3:]:
            print(f'{ticker} - {vol} %')
        print(f'Нулевая волатильность:')
        zero = sorted(self.secid_list_zero.keys(), key=lambda pair: pair[0], reverse=False)
        print(', '.join(zero))


@time_track
def main():
    mycsvdir = r'trades'
    gl_list = defaultdict(int)
    gl_list_zero = defaultdict(int)
    lock = threading.RLock()
    csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))
    volatilities = [Volatility(csvfile=csv, lock=lock, id_list=gl_list, id_list_zero=gl_list_zero) for csv in csvfiles]
    for volatility in volatilities:
        volatility.start()
    for volatility in volatilities:
        volatility.join()
    pr = Processing(gl_list, gl_list_zero)
    pr.file_processing()


if __name__ == '__main__':
    main()
