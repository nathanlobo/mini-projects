import random

targetNo = random.randint(1,100)

while True:
    userChoice = input("Guess the number or Quit:")
    if userChoice == "Quit":
        break
    userChoice = int(userChoice)
    if userChoice == targetNo:
        print("You Won")
    elif userChoice < targetNo:
        print("Your choice was too low, Guess again!")
    else:
        print("Your choice was too high, Guess again!")

print("----Game Over----")
