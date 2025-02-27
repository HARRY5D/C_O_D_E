
from datetime import datetime
import PYTHON.PRACTICAL.arith_module as a
import geo as b

def main():

    x =3
    y = 10
    print("Arithmetic Module:")
    print(f"  {x} + {y} = {a.add_numbers(x, y)}")
    print(f"  {x} is even? {a.is_even(x)}\n")

    now = datetime.now()
    print("Current Date/Time:")
    print("  ", now.strftime("%Y-%m-%d : %H:%M:%S"), "\n")

    print(f"  Area of circle (r=5): {b.calculate_area('circle', 5)}")
    print(f"  Area of rectangle (10x3): {b.calculate_area('rectangle', 10, 3)}")
    print(f"  Area of triangle (base=6, height=4): {b.calculate_area('triangle', 6, 4)}")
    print(f"  Is 29 prime? {b.is_prime(29)}")

if __name__ == "__main__":
    main()