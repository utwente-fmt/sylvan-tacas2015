Sylvan experiments
==================
This repository hosts the source code of the experimental section in the paper on [Sylvan](http://fmt.ewi.utwente.nl/tools/sylvan) submitted to TACAS 2015.

You can contact the main author of Sylvan at <t.vandijk@utwente.nl>.

Sylvan source code: https://github.com/utwente-fmt/sylvan  
LTSmin source code: https://github.com/utwente-fmt/ltsmin  
LTSmin install scripts for TACAS paper: https://github.com/utwente-fmt/ltsmin-tacas2014

Experiments
===========
To reproduce the results, use the `tacas2015` commit of LTSmin.

exp.py runs the following command on all models:

```
dve2lts-sym --when --vset=lddmc -rgs --lddmc-tablesize=30 --lddmc-cachesize=30 --order=<order> --lace-workers=<workers> models/<model>.dve
```

The results are stored in subdirectory exp-out

exp-sylvan.py runs the following command on all models:

```
dve2lts-sym --when --vset=sylvan -rgs --sylvan-tablesize=30 --sylvan-cachesize=30 --order=<order> --lace-workers=<workers> models/<model>.dve
```

The results are stored in subdirectory exp-sylvan

results.py generates results.csv

results-sylvan.py generates results-sylvan.csv
