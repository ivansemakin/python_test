class Fibo:
    def __init__(self):
        self.first_numb = 0
        self.second_numb = 1

    def __iter__(self):
        return self

    def __next__(self):
        fib_number = self.first_numb
        self.first_numb, self.second_numb = self.second_numb, self.first_numb + self.second_numb
        return fib_number

fib_class = Fibo()
fibo_iterator = iter(fib_class)
print([next(fibo_iterator) for n in range(20)]) 
print(next(fibo_iterator)) # Чтобы показать, что дальше итерируется

"""
Функция integers является генератором целых положительных чисел
"""

def integers():
    number = 0
    while True:
        yield number
        number += 1

gen = integers()
print([next(gen) for n in range(20)])
print(next(gen),next(gen))  # Чтобы показать, что дальше итерируется

"""
Функция primes является генератором простых чисел больше 1, делящихся только на самих себя и 1
"""

def primes():
    number = 2
    while True:
        flag_prime = True
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                flag_prime = False
                break        
        if flag_prime:
            yield number
        number += 1

prime_gen = primes()
print([next(prime_gen) for _ in range(20)]) 
print(next(prime_gen),next(prime_gen))