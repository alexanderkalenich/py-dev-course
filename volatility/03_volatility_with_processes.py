# -*- coding: utf-8 -*-


import glob
import multiprocessing
import os
import time
from collections import defaultdict
from queue import Empty


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result

    return surrogate


class Volatility(multiprocessing.Process):

    def __init__(self, csvfile, collector, id_list, id_list_zero, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csvfile = csvfile
        self.collector = collector
        self.csvfile = csvfile
        self.gl_list = id_list
        self.gl_list_zero = id_list_zero

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
            volatility_ = round(volatility_value, 2)
            self.collector.put(dict(secid=secid, volatility_=volatility_))


class Processing:

    def __init__(self, gl_list, gl_list_zero):
        self.secid_list = gl_list
        self.secid_list_zero = gl_list_zero

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


class SendFile(multiprocessing.Process):

    def __init__(self):
        super().__init__()
        self.collector = multiprocessing.Queue(maxsize=3)
        self.gl_list = defaultdict(int)
        self.gl_list_zero = defaultdict(int)

    @time_track
    def run(self):
        mycsvdir = r'trades'

        csvfiles = glob.glob(os.path.join(mycsvdir, '*.csv'))
        volatilities = [
            Volatility(csvfile=csv, collector=self.collector, id_list=self.gl_list,
                       id_list_zero=self.gl_list_zero) for csv in csvfiles]
        for volatility in volatilities:
            volatility.start()

        while True:
            try:
                data = self.collector.get(timeout=0.1)
                if data['volatility_'] == 0.0:
                    self.gl_list_zero[data['secid']] = data['volatility_']
                else:
                    self.gl_list[data['secid']] = data['volatility_']
            except Empty:
                if not any(volatility.is_alive() for volatility in volatilities):
                    break

        for volatility in volatilities:
            volatility.join()

        pr = Processing(self.gl_list, self.gl_list_zero)
        pr.file_processing()


if __name__ == '__main__':
    send = SendFile()
    send.start()
    send.join()
