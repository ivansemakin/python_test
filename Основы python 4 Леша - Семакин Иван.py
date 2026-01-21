quantity = int(input())
massive = [int(numb) for numb in input().split()] 
total_sum = sum(massive)
none_indexes = [i for i, x in enumerate(massive) if x != 0]
 
if not none_indexes:
    print("NO")
else:
    print("YES")
    print(len(none_indexes))
    for i in range(len(none_indexes)):
        if i == 0:
            left = 1
        else:
            left = none_indexes[i] + 1
        if i < len(none_indexes) - 1:
            right = none_indexes[i+1]
        else:
            right = quantity
        print(left, right)
        





        
        


