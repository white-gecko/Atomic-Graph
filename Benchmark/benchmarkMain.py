import subprocess
import os
import os.path
import sys


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
    result.wait()
    collect_data(result, collected_data)


def collect_data(result, collected_data):
    time_bygone = str(result.stdout.readline(), 'utf-8').strip()
    print(time_bygone)
    collected_data[0] += float(time_bygone)
    collected_data[1] += 1
    result.stdout.close()
    result.terminate()


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
        sortedFiles = sorted(files, key=lambda key: int(key.split("-")[2]))
        for name in sortedFiles:
            print("testing: " + os.path.join(path, name))
            test_colouring(os.path.join(path, name), RDFFormat[i],
                           collected_data)
print("results: " + str(collected_data[0]/collected_data[1]))



#subprocess.run(["python",
#                "benchmark_clean.py",
#                "../Examples/example1.ttl",
#                "-f",
#                "n3",
#                "../Examples/example2.ttl",
#                "-f",
#                "n3",
#                ])
#
#subprocess.run(["python",
#                "benchmark_clean.py",
#                "../../AtomicGraph Files/06/data.nq-0",
#                "-f",
#                "nquads",
#                "-t",
#                "colouring"
#                ])
#
#subprocess.run(["time",
#                "python",
#                "benchmark_dirty.py",
#                "../Examples/example1.ttl",
#                "-f",
#                "n3",
#                "../Examples/example2.ttl",
#                "-f",
#                "n3"
#                ])
#
#subprocess.run(["time",
#                "python",
#                "benchmark_dirty.py",
#                "../Examples/example1.ttl",
#                "-f",
#                "n3",
#                "-t",
#                "colouring"
#                ])
