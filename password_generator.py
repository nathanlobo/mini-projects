import random
import string

pass_len = 10
all_char = string.ascii_letters + string.digits + string.punctuation
password = ""

# # While loop method uncomment to test
# while len(password) <= pass_len:
#     password = password + random.choice(all_char)

# For loop method
for i in range(pass_len):
    password += random.choice(all_char)

print("Your random password is: ", password)