from __future__ import print_function
import os
import sys
import re
import models as _m
from subprocess32 import call,TimeoutExpired
import math
import time
import random
import itertools

NOTDONE=0
DONE=1
TIMEOUT=2

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

def run_experiment(name, args, timeout, filename):
    status, value = get_experiment(filename)
    if status == DONE: return
    if status == TIMEOUT and value >= int(timeout): return

    # remove output and timeout files
    if os.path.isfile(filename): os.unlink(filename)
    timeout_filename = "{}.timeout".format(filename)
    if os.path.isfile(timeout_filename): os.unlink(timeout_filename)

    print("Performing {}... ".format(name), end='')
    sys.stdout.flush()

    try:
        with open(filename, 'w+') as out:
            call(args, stdout=out, stderr=out, timeout=timeout)
    except KeyboardInterrupt:
        os.unlink(filename)
        print("interrupted!")
        sys.exit()
    except OSError:
        os.unlink(filename)
        print("OS failure! (missing executable?)")
        sys.exit()
    except TimeoutExpired:
        with open(timeout_filename, 'w') as to: to.write(str(timeout))
        print("timeout!")
    else:
        status, value = get_experiment(filename)
        if status == DONE: print("done in {} seconds!".format(value))
        else: print("not done!")
    time.sleep(2)

def prepare_experiments():
    orders = []
    #orders += ['par']
    orders += ['par-prev']
    #orders += ['bfs']
    orders += ['bfs-prev']
    #orders += ['chain-prev']

    models = [a for a,b in _m.models]

    workers = []
    workers += [1]
    workers += [48]
    workers += [16]
    workers += [24]
    #workers += [8]
    workers += [32]
    #workers += [40]

    experiments = []
    for w in workers:
        for o in orders:
            for m in models:
                experiments.append((m, o, ("dve2lts-sym","--when","--vset=lddmc","-rgs","--lddmc-tablesize=30","--lddmc-cachesize=30","--order={}".format(o),"--lace-workers={}".format(w),"models/{}.dve".format(m)), int(w)))

    return experiments

def existing_results(experiments, outdir):
    yes = 0
    no = 0
    timeout = 0

    for i in itertools.count():
        stop = True
        for name, order, call, workers in experiments:
            status, value = get_experiment("{}/{}-{}-{}-{}".format(outdir, name, order, workers, i))
            if not status == NOTDONE: stop = False
            if status == DONE: yes += 1
            elif status == TIMEOUT: timeout += 1
            else: no += 1
        if stop: return i, yes, no - len(experiments), timeout

def main():
    outdir = 'exp-out'
    if not os.path.exists(outdir): os.makedirs(outdir)

    experiments = prepare_experiments()

    n, yes, no, timeout = existing_results(experiments, outdir)
    print("In {} repetitions, {} succesful, {} timeouts, {} not done.".format(n, yes, timeout, no))

    for i in itertools.count():
        random.shuffle(experiments)
        for name, order, call, workers in experiments:
            run_experiment("{}-{}-{}".format(name, order, workers), call, 1200, "{}/{}-{}-{}-{}".format(outdir, name, order, workers, i))
        n, yes, no, timeout = existing_results(experiments, outdir)
        print("In {} repetitions, {} succesful, {} timeouts, {} not done.".format(n, yes, timeout, no))

if __name__ == "__main__":
    main()
