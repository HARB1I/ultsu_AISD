import re
nums = {'0':"ноль",'1':'один','2':'два',
        '3':'три','4':'четыре','5':'пять',
        '6':'шесть','7':'семь'}
k=1
with open("text.txt","r") as file:
    data = file.read()
    regul ="\d{1,5}[1357]"
    numbers = re.findall(regul, data)
    for number in numbers:
        if len(number) % 2 == 0 and len(number) > k:
            for i in number:
                print(nums.get(i), end = " ")
            print(" ")
            
