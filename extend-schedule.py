import random
import string

NUM_TEAMS = 12

numbers = list(range(1, NUM_TEAMS + 1))

random.shuffle(numbers)

mapping = {
    '_{}'.format(x): y
    for x, y in enumerate(numbers, start=1)
}

print(mapping)

with open('schedule-{}.txt'.format(NUM_TEAMS), mode='r+') as f:
    f.seek(0)
    existing = '{_' + f.read().replace('|', '}|{_').replace('\n', '}\n{_').strip('{_')
    new = existing.format(**mapping)
    print(new, file=f)
