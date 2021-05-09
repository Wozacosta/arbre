from itertools import cycle
import itertools
from time import sleep

for frame in cycle(r"-\|/"):
    print(f"\r{frame}", end="", flush=True)
    sleep(0.2)
