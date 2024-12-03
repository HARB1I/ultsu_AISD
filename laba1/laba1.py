#Вариант 23.
#Восьмиричные числа не превышающие 409610. Выводит на экран нечетные числа, содержащие четное количество цифр, превышающее К. 
#Список используемых цифр выводится отдельно прописью.


nums = {'0':"ноль",'1':'один','2':"два",
        '3':"три",'4':"четыре",'5':"пять",
        '6':"шесть",'7':"семь", '-':"минус"}
k = int(input("введите число k: "))
max_num = 4096
buf_len = 1
max_num_oct = int(oct(max_num)[2:])                                                            
work_buffer = ""
with open("text.txt","r") as file:
      buffer = file.read(buf_len)                                    
      while buffer:
           if buffer == '-':
              work_buffer += buffer
              buffer = file.read(buf_len)
           while buffer >= '0' and buffer <= '7':                                                            
              work_buffer += buffer
              buffer = file.read(buf_len)
           if len(work_buffer) > 0 and abs(int(work_buffer)) <= max_num_oct and abs(int(work_buffer)) % 2 == 1 and len(str(abs(int(work_buffer)))) % 2 == 0 and len(str(work_buffer)) > k:
                for x in str(work_buffer): 
                    print(nums[str(x)], end = " ")
                print(" ")
           work_buffer = ''
           buffer = file.read(buf_len)
              
                
      
                                    

        

