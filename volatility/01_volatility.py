# -*- coding: utf-8 -*-

import glob
import os
import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result

    return surrogate


class Volatility:
    secid_list = {}
    secid_list_zero = {}

    def __init__(self, csvfile):
        self.csvfile = csvfile

    def run(self):
        with open(self.csvfile, 'r', encoding='utf8') as ff:
            maximum = 0
            minimum = 0
            for line in ff:
                line = line[:-1]
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
            if volatility_value == 0:
                Volatility.secid_list_zero[secid] = round(volatility_value, 2)
            else:
                Volatility.secid_list[secid] = round(volatility_value, 2)


class Processing:

    def __init__(self):
        self.secid_list = Volatility.secid_list
        self.secid_list_zero = Volatility.secid_list_zero

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
    csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))
    for csvfile in csvfiles:
        volatility = Volatility(csvfile)
        volatility.run()
    pr = Processing()
    pr.file_processing()


if __name__ == '__main__':
    main()
