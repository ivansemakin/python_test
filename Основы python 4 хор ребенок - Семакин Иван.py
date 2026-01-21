import math

tests_numbers = int(input())
for i in range(tests_numbers):
    quantity_of_numbers = int(input()) 
    digits = [int(numb) for numb in input().split()]
    digits[min(enumerate(digits), key=lambda item: item[1])[0]] += 1
    print(math.prod(digits))