
def gen1(name: str):
    for i in name:
        yield i


def gen2(number: int):
    for i in range(number):
        yield i


g1 = gen1("Dmitry")
g2 = gen2(6)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        next_task = next(task)
        print(next_task)
        tasks.append(task)
    except StopIteration:
        pass

