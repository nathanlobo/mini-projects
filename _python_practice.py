# list = [1,2,3,2,1]
# listCopy = list.copy()
# listCopy.reverse()
# if list == listCopy:
#     print("Palindrome") #Palindrome is when a word(in this List of char) is the same even if reversed
# else:
#     print("Not a Palindrome")

# #Tuples
# grades = ("C","D","A","A","B","B","A")
# no_of_students = grades.count("A")
# print(no_of_students)

# #List
# grades = ["C","D","A","A","B","B","A"]
# grades.sort()
# print(grades)


# nums = []
# for val in nums:
#     print(val)
# else:
#     print("Done")

# #multiplication
# num = int(input("Enter number to check it table:"))
# print(type(num))
# for i in range(1,11):
#     print(num*i)


# for i in range(1,11,5):
#     print(i)

# i=1
# sum=0
# n=int(input("enter n:"))
# while i<=n:
#     sum=sum+i
#     i+=1
# print("Sum =",sum)

# i=1
# fact=1
# n=int(input("enter n:"))
# while i<=n:
#     fact=fact*i
#     i+=1
# print("Factorial =",fact)


# n=int(input("Enter:"))
# def sum_of_numbers(n):
#     if n==0:
#         return 0
#     return sum_of_numbers(n-1) + n
# print(sum_of_numbers(n))


# list = ["apple","ball"]
# def print_list(list,idx=0):
#     if(idx == len(list)):
#         return
#     print(list[idx])
#     print_list(list, idx+1)
# print_list(list)

# f = open("hi.txt","r")
# data = f.read()
# print(data)
# f.close()

# with open("practice.txt", "w") as f:
#     f.write("Hi everyone\nwe are learning file I/O\nusing Java\nI like programming in Java")

# #reached at 7:39:05

# with open("practice.txt", "r") as f:
#     data = f.read()
# new_data = data.replace("Java","Python")
# print(new_data)

# with open("practice.txt", "w") as f:
#     f.write(new_data)

# def chk_word():
#     word = "learning"
#     with open("practice.txt", "r") as f:
#         data = f.read()
#         if data.find(word) != -1:
#             print("Found")
#         else:
#             print("Not found")
# chk_word()

# def chk_line():
#     word = "like"
#     data = True
#     lineNo = 1
#     with open("practice.txt", "r") as f:
#         while data:
#             data = f.readline()
#             if word in data:
#                 print(lineNo)
#                 return
#             lineNo+=1
#     return -1
# chk_line()


class order:
    def __init__(self, item, price):
        self.item = item
        self.price = price
    
    def __gt__(self, odr2):
        return self.price > odr2.price


odr1 = order("Chips", 20)
odr2 = order("Tea", 15)

print(odr1 > odr2)
