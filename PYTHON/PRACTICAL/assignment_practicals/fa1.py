def generate_squares(n):
    return {i: i*i for i in range(1, n+1)}

n = int(input("Enter a number: "))
result = generate_squares(n)
print(result)