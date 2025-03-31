
import math

def calculate_area(shape, *dim):
   
    if shape.lower() == 'circle':
        radius = dim[0]
        return math.pi * (radius ** 2)
    elif shape.lower() == 'rectangle':
        length, width = dim
        return length * width
    elif shape.lower() == 'triangle':
        base, height = dim
        return 0.5 * base * height
    else:
        return None

def is_prime(n):

    if n < 2:
     return False
    if n % 2 == 0:
        return False
    return True