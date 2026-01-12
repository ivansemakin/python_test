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


# test
print("test")

d1 = 8
d2 = 10
h = 50
v_sand = 5
n = 2
q = 0
t_min = {}
for i in range(100):
    # q = 39.413
    q = q + 1
    t, q = calc(d1, d2, h, v_sand, n, q)
    print("Если спасатель начнёт движение под углом theta1, равным " + str(
        q) + " градусам, он достигнет утопащего через " + str(t) + " секунды")
    t_min[q] = t
min_time = min(t_min.items(), key=lambda item: item[1])
print("Минимальное время до утопающего: ", str(min_time[1]), "сек. наступит, если он начнет движение под углом theta1, равным: ", str(min_time[0]), " градусам")
