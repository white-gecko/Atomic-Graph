import subprocess

subprocess.run(["python",
                "benchmark_clean.py",
                "../Examples/example1.ttl",
                "-f",
                "n3",
                "../Examples/example2.ttl",
                "-f",
                "n3",
                ])

subprocess.run(["python",
                "benchmark_clean.py",
                "../../AtomicGraph Files/08/data.nq-0",
                "-f",
                "nquads",
                "-t",
                "colouring"
                ])

subprocess.run(["time",
                "python",
                "benchmark_dirty.py",
                "../Examples/example1.ttl",
                "-f",
                "n3",
                "../Examples/example2.ttl",
                "-f",
                "n3"
                ])

subprocess.run(["time",
                "python",
                "benchmark_dirty.py",
                "../Examples/example1.ttl",
                "-f",
                "n3",
                "-t",
                "colouring"
                ])
