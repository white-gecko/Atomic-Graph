
## Install Requirements

    mkvirtualenv -p /usr/bin/python3 -r requirements.txt atomicgraphs

## Execute the Benchmark

1. Download `http://aidanhogan.com/skolem/eval.zip`
2. unzip `eval.zip`
3. go to `benchmarks`
4. run `python3 benchmarkMain.py ../eval/ -f graph`

If you just want to benchmark a subset of the eval, just create a different folder, e.g. `eval-small` and move one of the sub folders (e.g. `mz`) from `eval` to this folder.

To visualize the evaluation graphs you convert them to GraphViz dot:

e.g. convert `mz-2`

```
p edge 40 60
e 1 3
e 1 8
e 1 9
e 2 4
```

to `mz-2.dot`
```
digraph mz2 {
1->3;
1->8;
1->9;
2->4;
...
}
```
