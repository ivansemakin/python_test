import math

""" 
RatNum - класс являющийся АСД, на вход получающий строку, далее ее преобразующий в числитель и знаменатель
Основные функции класса: проверки является ли числом, отрицательным , положительным, сравнение чисел, перевод к типам с integer и float,
    аддитивная инверсия, сложение, вычитание, умножение, деление, НОД двух чисел, приведение к строковому типу, подсчет хеш суммы и проверка на эквивалентность 
"""
class RatNum:
    def __init__(self, input_data, den=1):
        try:
            # Обработка входных данных
            if isinstance(input_data, str):
                clean_input = input_data.replace(" ", "").upper()
                if clean_input == "NaN":
                    self._num, self._den = float('NaN'), 0
                    return
                if '/' in clean_input:
                    n_str, d_str = clean_input.split('/')
                    num, den = int(n_str), int(d_str)
                else:
                    num, den = int(clean_input), 1
            else:
                num = input_data

            # Логика NaN
            if den == 0 or (isinstance(num, float) and math.isnan(num)):
                self._num, self._den = float('NaN'), 0
                return

            # Сокращение дроби 
            common = math.gcd(num, den)
            self._num = num // common
            self._den = den // common

            if self._den < 0:
                self._num, self._den = -self._num, -self._den
        except (ValueError, TypeError, ZeroDivisionError):
            self._num = float('NaN')
            self._den = 0

    
    def gcd(self, other):
        """Находит НОД двух рациональных чисел: gcd(a/b, c/d) = gcd(a,c) / lcm(b,d)"""
        if self.is_nan() or other.is_nan():
            return RatNum("NaN")
        
        num_gcd = math.gcd(self._num, other._num)
        # lcm(b, d) = (b * d) // gcd(b, d)
        den_lcm = (self._den * other._den) // math.gcd(self._den, other._den)
        
        return RatNum(num_gcd, den_lcm)

    def is_nan(self):
        """Проверка является ли NaN"""
        return math.isnan(self._num)

    def is_negative(self):
        """Проверка является ли отрицательным число"""
        return not self.is_nan() and self._num < 0

    def is_positive(self):
        """Проверка является ли положительным число"""
        return not self.is_nan() and self._num > 0

    def compare_to(self, other):
        """Cравнение какое из чисел больше,если первое то 1 ,если второе -1 ,если равны то возвращаем 0"""
        if self.is_nan():
            return 0 if other.is_nan() else 1
        if other.is_nan():
            return -1
        diff = self._num * other._den - other._num * self._den
        return (diff > 0) - (diff < 0)

    def float_value(self):
        """Переводим число с плавающей точкой"""
        return self._num / self._den if not self.is_nan() else float('NaN')

    def int_value(self):
        """Переводим число в целочисленное"""
        return int(self.float_value()) if not self.is_nan() else None

    
    def __neg__(self):
        """Производим аддитивную инверсию числа в отрицательное или положительное"""
        return RatNum(-self._num, self._den) if not self.is_nan() else self

    def __add__(self, other):
        """Производим сложение двух чисел"""
        if self.is_nan() or other.is_nan(): 
            return RatNum("NaN")
        return RatNum(self._num * other._den + other._num * self._den, self._den * other._den)

    def __sub__(self, other):
        """Производим вычитание двух чисел"""
        return self + (-other)

    def __mul__(self, other):
        """Производим умножение двух чисел"""
        if self.is_nan() or other.is_nan(): 
            return RatNum("NaN")
        return RatNum(self._num * other._num, self._den * other._den)

    def __truediv__(self, other):
        """Производим деление двух чисел"""
        if self.is_nan() or other.is_nan() or other._num == 0: 
            return RatNum("NaN")
        return RatNum(self._num * other._den, self._den * other._num)

    def __str__(self):
        """Приводим к строковому виду"""
        if self.is_nan(): 
            return "NaN"
        return f"{self._num}/{self._den}" if self._den != 1 else str(self._num)

    def __eq__(self, other):
        """Проверка эквивалентности"""
        if self.is_nan() and other.is_nan(): 
            return True
        if self.is_nan() or other.is_nan(): 
            return False
        return self._num == other._num and self._den == other._den

    def __hash__(self):
        """Подсчет хеша"""
        return hash((self._num, self._den))
    


""" 
RatPoly - класс являющийся АСД, на вход получающий строку, далее ее преобразующий в полином (можно и такого типа "1/2 0 5")
Основные функции класса: проверки на NaN, нормализация , возвращение степени полинома, сравнение полиномов, возвращение коэффициента при заданной степени,
    аддитивная инверсия, сложение, вычитание, умножение, деление, умножение на скалярное значение, приведение к строковому типу, подсчет производной и первообразной полинома, подсчет хеш суммы и проверка на эквивалентность 
"""

class RatPoly:
    def __init__(self, coeffs_data=None):
        self.coeffs = []

        # Обработка данных
        if isinstance(coeffs_data, str):
            clean_data = coeffs_data.strip()
            if clean_data.upper() == "NaN":
                self.coeffs = [RatNum("NaN")]
            else:
                # Разрезаем строку по пробелам и каждую часть отдаем в RatNum
                parts = clean_data.split()
                self.coeffs = [RatNum(p) for p in parts]
        
        # Если на вход пришел список
        elif isinstance(coeffs_data, list):
            self.coeffs = [c if isinstance(c, RatNum) else RatNum(c) for c in coeffs_data]       
        # Если ничего не пришло (нулевой полином)
        else:
            self.coeffs = [RatNum(0)]

        self._normalize()

    def _normalize(self):
        """Удаляем лишние нули в конце и проверяем на наличие NaN внутри"""
        if any(c.is_nan() for c in self.coeffs):
            self.coeffs = [RatNum("NaN")]
            return
        
        while len(self.coeffs) > 1 and self.coeffs[-1] == RatNum(0):
            self.coeffs.pop()

    def is_nan(self):
        return any(c.is_nan() for c in self.coeffs)

    def degree(self):
        """Возвращаем степень полинома"""
        if self.is_nan(): 
            return 0
        return len(self.coeffs) - 1

    def get_coeff(self, deg):
        """Возвращаем коэффициент при заданной степени"""
        if deg < 0 or deg >= len(self.coeffs):
            return RatNum(0)
        return self.coeffs[deg]

    def scale_coeff(self, scalar):
        """Умножаем весь полином на число (RatNum или строка)"""
        s = scalar if isinstance(scalar, RatNum) else RatNum(scalar)
        if self.is_nan() or s.is_nan(): 
            return RatPoly("NaN")
        return RatPoly([c * s for c in self.coeffs])

    def __neg__(self):
        """Унарный минус (аддитивная инверсия)."""
        return RatPoly([-c for c in self.coeffs])

    def __add__(self, other):
        """Производим сложение двух полиномов"""
        if self.is_nan() or other.is_nan(): 
            return RatPoly("NaN")
        size = max(len(self.coeffs), len(other.coeffs))
        new_coeffs = []
        for i in range(size):
            new_coeffs.append(self.get_coeff(i) + other.get_coeff(i))
        return RatPoly(new_coeffs)

    def __sub__(self, other):
        """Производим вычитание двух полиномов"""
        return self + (-other)

    def __mul__(self, other):
        """Производим умножение двух полиномов"""
        if self.is_nan() or other.is_nan(): 
            return RatPoly("NaN")
        # Степень произведения = сумма степеней
        res_size = self.degree() + other.degree() + 1
        res = [RatNum(0)] * res_size
        for i, c1 in enumerate(self.coeffs):
            for j, c2 in enumerate(other.coeffs):
                res[i+j] = res[i+j] + (c1 * c2)
        return RatPoly(res)

    def __truediv__(self, other):
        """Производим деление полиномов только если один из полиномов 0 степени """
        if other.degree() == 0:
            return self.scale_coeff(RatNum(1) / other.get_coeff(0))
        return RatPoly("NaN") # В рамках базовой АСД
    
    def eval(self, x):
        """Вычисляем значение P(x). Входное значение должно быть RatNum"""
        if self.is_nan() or x.is_nan(): 
            return RatNum("NaN")
        res = RatNum(0)
        for i, coeff in enumerate(self.coeffs):
            # Считаем coeff * x^i
            pwr = RatNum(1)
            for _ in range(i): 
                pwr = pwr * x
            res = res + (coeff * pwr)
        return res

    def differentiate(self):
        """Производная полинома"""
        if self.is_nan(): 
            return RatPoly("NaN")
        if self.degree() == 0: 
            return RatPoly([RatNum(0)])
        new_coeffs = []
        for i in range(1, len(self.coeffs)):
            new_coeffs.append(self.coeffs[i] * RatNum(i))
        return RatPoly(new_coeffs)

    def anti_differentiate(self, constant=RatNum(0)):
        """Первообразная полинома"""
        if self.is_nan(): return RatPoly("NaN")
        c = constant if isinstance(constant, RatNum) else RatNum(constant)
        new_coeffs = [c]
        for i, coeff in enumerate(self.coeffs):
            new_coeffs.append(coeff / RatNum(i + 1))
        return RatPoly(new_coeffs)

    def integrate(self, a, b):
        """Нахождение интеграла на отрезке [a, b]. a, b - RatNum."""
        antidiff = self.anti_differentiate()
        return antidiff.eval(b) - antidiff.eval(a)

    def __str__(self):
        """Приводим к строковому виду"""
        if self.is_nan(): 
            return "NaN"
        if self.coeffs == [RatNum(0)]: 
            return "0"
        res = []
        for i in range(len(self.coeffs) - 1, -1, -1):
            c = self.coeffs[i]
            if c == RatNum(0): 
                continue
            term = f"({c})"
            if i > 0: term += f"*x^{i}"
            res.append(term)
        return " + ".join(res)

    def __eq__(self, other):
        """Проверка эквивалентности"""
        if self.is_nan() and other.is_nan(): 
            return True
        if self.is_nan() or other.is_nan(): 
            return False
        return self.coeffs == other.coeffs

    def __hash__(self):
        """Подсчет хеша"""
        return hash(tuple(self.coeffs))

    @staticmethod
    def value_of(poly_str):
        """Принимаем строку и возвращаем новый объект RatPoly"""
        if not isinstance(poly_str, str):
            return RatPoly("NaN")
            
        clean_str = poly_str.strip()
        if not clean_str:
            return RatPoly([0]) 
        return RatPoly(clean_str)


    
if __name__ == '__main__':
    number = input("Первое число: ")
    another = input("Второе число: ")
    rat_number = RatNum(number)
    another_rat_numb = RatNum(another)
    print(rat_number._num,rat_number._den)
    print(rat_number.is_nan(),rat_number.is_negative(),rat_number.is_positive())
    print(rat_number.float_value(),rat_number.int_value(),rat_number.__neg__(),rat_number.__str__(),rat_number.__hash__())
    print("__add__ - ",rat_number.__add__(another_rat_numb)," __sub__ - ",rat_number.__sub__(another_rat_numb)," __mul__ - ",rat_number.__mul__(another_rat_numb)," __truediv__ - ",
        rat_number.__truediv__(another_rat_numb)," __eq__ - ",rat_number.__eq__(another_rat_numb)," gcd - ",rat_number.gcd(another_rat_numb)," compare - ",rat_number.compare_to(another_rat_numb))

    poly1 = RatPoly("1/4 0 3/5") 
    poly2 = RatPoly([RatNum(0), RatNum("1/2")])
    poly3 = RatPoly("123fdsgfds")
    poly4 = RatPoly.value_of("1/3 2 5/18") 
    print(poly1,poly2,poly3,poly4)
    print(poly2.is_nan(),poly2._normalize(),poly2.degree())
    print(poly2.get_coeff(4),poly2.get_coeff(1),poly2.scale_coeff(rat_number),poly2.__neg__(),poly2.__str__(),poly2.__hash__(),poly2.eval(another_rat_numb))
    print("__add__ - ",poly2.__add__(poly4)," __sub__ - ",poly2.__sub__(poly4)," __mul__ - ",poly2.__mul__(poly4)," __truediv__ - ",
        poly4.__truediv__(poly2)," __eq__ - ",poly2.__eq__(poly4)," anti_differentiate - ",poly2.anti_differentiate(rat_number)," integrate - ",poly2.integrate(rat_number,another_rat_numb)," differentiate - ",poly2.differentiate())

