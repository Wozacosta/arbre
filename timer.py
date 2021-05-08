import time

num_seconds = 3
for countdown in reversed(range(num_seconds + 1)):
    if countdown > 0:
        print(countdown, end='', flush=True)
        for _ in range(5):
            print('.', end='', flush=True)
            time.sleep(0.17)
        time.sleep(0.17)
    else:
        print('Go!')
