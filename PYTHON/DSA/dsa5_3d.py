from collections import deque

def generate_binary_numbers(n):
    result = []
    queue = deque(["1"])

    for i in range(n):
        binary = queue.popleft()
        result.append(binary)

        queue.append(binary + "0")
        queue.append(binary + "1")
    return result

def number():
    n = int(input("ENTER VALUE OF N : "))
    binary_numbers = generate_binary_numbers(n)
    
    print(f"BINARY NUMBERS FROM 1 TO {n}:")
    for i, t in enumerate(binary_numbers, start=1):
        print(f"{i} : {t}")

number()