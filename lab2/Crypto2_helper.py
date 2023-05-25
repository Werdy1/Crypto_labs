import time
import random

def generate_equation(order: int):
    pass

while 1:
    print("Welcome, please enter 1 when you are ready\n"\
          "1 - try_method\n"\
          "2 - silver_polig_hellman_method\n"\
          "0 - Exit"\
          )
    n = input()
    if n == "1":
        order = int(input("Please, enter your p number (prime number) order :"))
        start = time.time()
        result = generate_equation(order)
        end = time.time()
        print(result)
        print("It takes:",end - start,"seconds")
    elif n == "0":
        break
    else:
        print("Can't understand what do you want. Please, try againg")
