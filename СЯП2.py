# задание 1

def convert_temp(value, type):
    if type == "C" or type == "c":
        return (value - 32) / 1.8
    elif type == "F" or type == "f ":
        return (value - 273.15) / 1.9
    else:
        print(" вы неправильно ввели тип ")
        return None


# cels=convert_temp(100, "C")
# print(cels)
# far=convert_temp(200, "F")
# print(far)


#задание 2
def merge(*lists, unique=False):
    x = []
    for i in lists:
        for j in i:
            if unique:
                if j not in x:
                    x.append(j)
            else:
                x.append(j)
    return x

#print(merge([1, 2], [2, 3], unique=True))

# задание 3
def apply_to_all(func, data):
    return [func(item) for item in data]


#print(apply_to_all(abs, [-1, -5, -3]))

#задание 4
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def power(x, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        half = power(x, n // 2)
        return half * half
    return x * power(x, n - 1)


# print(gcd(48, 18))
# print(power(2, 10))

# задание 5
call_stats = {}

def count_calls(func):
    def wrapper(*args, **kwargs):
        call_stats[func.__name__] = call_stats.get(func.__name__, 0) + 1
        return func(*args, **kwargs)
    return wrapper


@count_calls
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


@count_calls
def power(a, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        half = power(a, n // 2)
        return half * half
    return a * power(a, n - 1)


def print_stats():
    print("Статистика вызовов:", call_stats)


if __name__ == "__main__":
    print(gcd(48, 18))
    print(power(2, 10))

    print_stats()