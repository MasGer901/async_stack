

def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


def subgen():
    x = "ready to accept message"
    message = yield x
    print(f"message is {message}")


class SomeException(Exception):
    pass


@coroutine
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print("Done")
            break
        except SomeException:
            print('SomeException')
            break
        else:
            count += 1
            summ += x
            average = round(summ/count, 2)

    return average



