from __future__ import print_function
import csv
import os
import sys
import re
import models as _m
from subprocess32 import call,TimeoutExpired
import math
import time
import random
import itertools

from exp import *

def extract(content, thing, letter):
    s = re.compile(re.escape(thing)+r'[:\W]*([\d\.]+)').findall(content)
    return len(s) == 1 and {letter: s[0]} or {}

def process_result(content):
    times = {}
    for a,b in [(r"reachability took","Ti"),
                (r"Steal work (sum):","Sw"), (r"Leap work (sum)","Lw"), 
                (r"Steal overhead (sum)","So"), (r"Leap overhead (sum)","Lo"), 
                (r"Steal search (sum)","Ss"), (r"Leap search (sum)","Ls")]:
        times.update(extract(content, a, b))
    return times

def online_variance(data):
    n = 0
    mean = 0
    M2 = 0

    for x in data:
        n = n + 1
        delta = x - mean
        mean = mean + delta/n
        M2 = M2 + delta*(x - mean)

    if n < 2: return n, mean, float('nan')

    variance = M2/(n - 1)
    return n, mean, variance

def get_experiment(filename):
    if (os.path.isfile(filename)):
        with open(filename, 'r') as res:
            s = re.compile(r'reachability took ([\d\.]+)').findall(res.read())
            if len(s) == 1: return DONE, float(s[0])

    timeout_filename = "{}.timeout".format(filename)
    if (os.path.isfile(timeout_filename)):
        with open(timeout_filename, 'r') as to:
            return TIMEOUT, int(to.read())

    return NOTDONE, 0

def report(results):
    names = set([name for name, workers, result in results])
    for exp in sorted(names):
        workers_in_data = set([workers for name, workers, result in results if name==exp])
        mean_1 = None
        for w in sorted(workers_in_data):
            data = [result for name, workers, result in results if name==exp and workers==w]
            n, mean, variance = online_variance(data)
            stdev = math.sqrt(variance)
            sem = math.sqrt(variance / n)
            if w == 1: mean_1 = mean
            if w != 1 and mean_1: speedup = "speedup={}".format(mean_1/mean)
            else: speedup = ""
            print("{0:<32}: {1:<8.2f} var={2:<6.2f} se={3:<6.2f} n={4:<5d} {5}".format(exp+"-"+str(w), mean, variance, sem, n, speedup))

def report2(results, timeouts):
    print("{0:<20} | {1:<10}   {2:<6}   {3:<6}   {4:<6}".format("Model", "Order", "T_1", "T_48", "Speedup"))
    #names = set([name for name, order, workers, result in results])
    names = [a for a,b in _m.models]
    for exp in sorted(names):
        #orders = set([order for name, order, workers, result in results if name==exp])
        orders = ['par-prev','bfs-prev',]
        for o in sorted(orders):
            n_1, mean_1, var_1 = online_variance([r for name, order, workers, r in results if name==exp and order == o and workers==1])
            if n_1 == 0:
                mean_1 = float('nan')
                to_1 = [r for name, order, workers, r in timeouts if name==exp and order == o and workers == 1]
                if len(to_1) > 0:
                    to_1 = min(to_1)
                    str_1 = ">{:d}".format(int(to_1))
                else:
                    to_1 = 0
                    str_1 = "N/A"
            else: str_1 = "{:<6.2f}".format(mean_1)

            n_48, mean_48, var_48 = online_variance([r for name, order, workers, r in results if name==exp and order == o and workers==48])
            if n_48 == 0: 
                mean_48 = float('nan')
                to_48 = [r for name, order, workers, r in timeouts if name==exp and order == o and workers == 48]
                if len(to_48) > 0:
                    to_48 = min(to_48)
                    str_48 = ">{:d}".format(int(to_48))
                else:
                    to_48 = 0
                    str_48 = "N/A"
            else: str_48 = "{:<6.2f}".format(mean_48)

            if mean_48 != 0: speedup = mean_1/mean_48
            else: speedup = float('nan')

            print("{0:<20} | {1:<10}   {2:<6}   {3:<6}   {4:<6.2f}".format(exp, o, str_1, str_48, speedup))

def all_experiments():
    orders = ['par','par-prev','bfs','bfs-prev',]
    models = [a for a,b in _m.models]
    workers = [1,2,4,8,16,32,40,48,56,64,]

    orders = ['par-prev','bfs-prev',]
    workers = [1,16,24,32,48,]

    for w in workers:
        for o in orders:
            for m in models:
                yield m, o, int(w)

def existing_results(experiments, outdir):
    results = []
    timeouts = []
    yes = 0
    no = 0
    timeout = 0

    for i in itertools.count():
        stop = True
        for name, order, call, workers in experiments:
            status, value = get_experiment("{}/{}-{}-{}-{}".format(outdir, name, order, workers, i))
            if not status == NOTDONE: stop = False
            if status == DONE: results.append((name, order, workers, value))
            elif status == TIMEOUT: timeouts.append((name, order, workers, value))
            else: no += 1
        if stop: return i, no - len(experiments), results, timeouts

def main():
    outdir = 'exp-out'
    if os.path.exists(outdir):
        experiments = prepare_experiments()
        n, no, results, timeouts = existing_results(experiments, outdir)
        print("In {} repetitions, {} succesful, {} timeouts, {} not done.".format(n, len(results), len(timeouts), no))
        with open('results.csv','wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(results)
        report2(results, timeouts)

if __name__ == "__main__":
    main()
