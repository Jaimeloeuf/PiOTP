import psutil
import os

val = (psutil.Process(os.getpid()).memory_info().rss) / 1024 / 1024  # in KB
print(val)
