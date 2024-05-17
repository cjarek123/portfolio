def func4(a, b, c):
    answer = c - b
    temp = answer
    temp = temp >> 31
    answer += temp
    answer = answer // 2
    temp = answer + b
    if temp > a:
        c = temp - 1
        answer = func4(a, b, c)
        answer = answer * 2
    else:
        answer = 0
        if temp < a:
            b = temp + 1
            answer = func4(a, b, c)
            answer = (answer * 2) + 1
    return answer


def main():
    tests = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    for test in tests:
        print(test)
        print(func4(0, 14, test))

if __name__ == "__main__":
    main()
    