from time import sleep

def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print(f"\r[{'#' * left}{' ' * right}] {percent:.0f}%", end='')

for i in range(101):
    progress(i)
    sleep(0.1)
