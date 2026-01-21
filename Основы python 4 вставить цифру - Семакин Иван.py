
Posses_number = int(input())
for i in range(Posses_number):
    length_and_bonus_number = [int(numb) for numb in input().split()] 
    data_number = input()
    data_list = [int(numb) for numb in data_number]
    data_list_stroke = ""
    flag_insert = False
    for j in range(length_and_bonus_number[0]):
        if length_and_bonus_number[1] > int(data_list[j]):
            data_list.insert(j, length_and_bonus_number[1])
            for dl in range(len(data_list)):
                data_list_stroke = data_list_stroke + str(data_list[dl])
            print(data_list_stroke)
            flag_insert = True
            break
    if not flag_insert:
        for dl in range(len(data_list)):
            data_list_stroke = data_list_stroke + str(data_list[dl])
        data_list_stroke = data_list_stroke + str(length_and_bonus_number[1])
        print(data_list_stroke)

