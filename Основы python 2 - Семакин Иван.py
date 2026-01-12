import math


def calc(d1, d2, h, v_sand, n, q):
    d1 = d1 * 3
    q_rad = math.radians(q)
    h = h * 3
    v_sand = v_sand * 5280 / 3600
    x = d1 * math.tan(q_rad)
    l1 = math.sqrt((x ** 2) + (d1 ** 2))
    l2 = math.sqrt(((h - x) ** 2) + (d2 ** 2))
    v_swim = v_sand / n
    t = (1 / v_sand) * (l1 + n * l2)
    
    t = round(t, 1)
    q = int(q)
    return t, q
    

d1 = float(input('d1: '))
d2 = float(input('d2: '))
h = float(input('h: '))
v_sand = float(input('v_sand: '))
n = float(input('n: '))
q = float(input('q: '))

t, q = calc(d1, d2, h, v_sand, n, q)

print("Если спасатель начнёт движение под углом theta1, равным " + str(q) + " градусам, он достигнет утопащего через " + str(t) + " секунды")

# test
print("test")

d1 = 8
d2 = 10
h = 50
v_sand = 5
n = 2
q = 39.413

t, q = calc(d1, d2, h, v_sand, n, q)

print("Если спасатель начнёт движение под углом theta1, равным " + str(q) + " градусам, он достигнет утопащего через " + str(t) + " секунды")