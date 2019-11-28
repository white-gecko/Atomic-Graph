import subprocess
import os
import os.path
import sys
import __main__


def test_colouring(graph_path, graph_format, collected_data,
                   dirty=False):
    if(dirty):
        testfile = "benchmark_dirty.py"
    else:
        testfile = "benchmark_clean.py"
    result = subprocess.Popen([
        "python",
        testfile,
        graph_path,
        "-f",
        graph_format,
        "-t",
        "colouring"
    ], stdout=subprocess.PIPE)
    try:
        result.wait(timeout=600)
        collect_data(result, collected_data)
    except subprocess.TimeoutExpired:
        store_data("-600", collected_data)


def collect_data(result, collected_data):
    store_data(str(result.stdout.readline(), 'utf-8').strip(), collected_data)
    result.stdout.close()
    result.terminate()


def store_data(data, collected_data):
    output(str(data))
    collected_data[0] += float(data)
    collected_data[1] += 1


def output(line):
    __main__.outputFile.write("{} \n".format(line))
    print(line)


outputFile = open("BenchmarkResults.txt", "w")
RDFFormat = []
graphs = []
testType = ""
flag = ""
collected_data = [0.0, 0]
skipFirst = True
for arg in sys.argv:
    if(skipFirst):
        skipFirst = False
        continue
    # set flag for next parameter
    if(arg[0] == "-"):
        flag = arg
        continue
    # use set flag parameter
    if(flag == "-f"):
        RDFFormat.append(arg)
        flag = ""
        continue
    graphs.append(arg)

for i in range(0, len(graphs)):
    for path, subdirs, files in os.walk(graphs[i]):
        sortedFiles = sorted(files, key=lambda key: int(key.split("-")[-1]))
        for name in sortedFiles:
            output("testing: " + os.path.join(path, name))
            test_colouring(os.path.join(path, name), RDFFormat[i],
                           collected_data)
output("results: " + str(collected_data[0] / collected_data[1]))
outputFile.close()
