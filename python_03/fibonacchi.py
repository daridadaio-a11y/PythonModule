

def fibo(total):
    a = 0
    b = 1
    for i in range(total):
        yield(a + b)
        tmp = b
        b = a + b
        a = tmp

def main():
    total = 10
    f = fibo(total)
    for num in f:
        print(f"{num}, ", end = "")


main()