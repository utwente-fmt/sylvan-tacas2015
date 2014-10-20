Sylvan experiments
==================
Sylvan is a parallel (multi-core) BDD library in C. Sylvan allows both sequential and parallel BDD-based algorithms to benefit from parallelism. Sylvan uses the work-stealing framework Lace and a scalable lockless hashtable to implement scalable multi-core BDD operations.

Sylvan is developed (&copy; 2011-2014) by the [Formal Methods and Tools](http://fmt.ewi.utwente.nl/) group at the University of Twente as part of the MaDriD project, which is funded by NWO. Sylvan is licensed with the Apache 2.0 license.

You can contact the main author of Sylvan at <t.vandijk@utwente.nl>.

Sylvan source code: https://github.com/trolando/sylvan

LTSmin source code: https://github.com/utwente-fmt/ltsmin

LTSmin install scripts for TACAS paper: https://github.com/utwente-fmt/ltsmin-tacas2014

Experiments
===========
exp.py runs the following command on all models:

`dve2lts-sym --when --vset=lddmc -rgs --lddmc-tablesize=30 --lddmc-cachesize=30 --order=<order> --lace-workers=<workers> models/<model>.dve`

The results are stored in subdirectory exp-out

exp-sylvan.py runs the following command on all models:

`dve2lts-sym --when --vset=sylvan -rgs --sylvan-tablesize=30 --sylvan-cachesize=30 --order=<order> --lace-workers=<workers> models/<model>.dve`

The results are stored in subdirectory exp-sylvan

results.py generates results.csv

results-sylvan.py generates results-sylvan.csv
