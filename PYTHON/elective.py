'''

#a
flowers = ["ROSE", "LILY", "LOTUS", "DAISY", "TULIP"]
print("ORIGINAL LIST :")
print(flowers)
#b
print("\n2ND ELEMENT :")
print(flowers[1])
#c
print("\n3RD & SUBSEQUENT ELEMENTS :")
print(flowers[2:])
#d
flowers[1] = "HIBISCUS"
print("\nLIST AFTER REPLACING 2ND ELEMENT :")
print(flowers)

flowers = ["ROSE", "HIBISCUS", "SUNFLOWER", "DAISY", "TULIP"]
print("PRINTING ELEMENTS USING FOR LOOP:")
for flower in flowers:
    print(flower)


element = []
while True:
    element = input("ENTER AN ELEMENT (OR 'Q' TO QUIT):")
    if element.lower() == 'q':
        break
    element.append(element)
    print("\nCURRENT LIST :")
    print(element)


def sort(nums):
    n = len(nums)
    for i in range(n-1):
        for j in range(n-i-1):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums

numbers = [64, 34, 25, 12, 22, 11, 90]
print("ORIGINAL LIST :")
print(numbers)
sorted_numbers = sort(numbers)
print("\nSORTED LIST :")
print(sorted_numbers)


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

n = int(input("ENTER THE NUMBER OF PRIME NUMBERS TO GENERATE : "))
prime_count = 0
num = 2
while prime_count < n:
    if is_prime(num):
        print(num)
        prime_count += 1
    num += 1


    
    '''
'''
def fibonacci(n):
    series = [0, 1]
    while len(series) < n:
        series.append(series[-1] + series[-2])
    return series

n = int(input("ENTER TOTAL NO. OF TERMS YOU WANT IN FIBONACCI SERIES : "))
print(fibonacci(n))
'''
def sort():
    n = int(input("ENTER TOTAL NO. OF ELEMENT: "))
    element = []
    for i in range(n):
        num = float(input(f"ENTER ELEMENT {i+1}: "))
        element.append(num)
    element.sort(reverse=True)
    print("SORTED LIST [DESCENDING ORDER] :", element)

sort()