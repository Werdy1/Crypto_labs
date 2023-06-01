import time
def index_calculus():
    #
    c = 3.38
    pass

while 1:
    print("Welcome, please enter 1 when you are ready\n"\
          "1 - ready\n"\
          "0 - Exit"\
          )
    n = input()
    if n == "1":
        a = int(input("Please, enter your a number (generator):"))
        b = int(input("Please, enter your b number (field element):"))
        p = int(input("Please, enter your p number (prime number):"))
        print()
    elif n == "0":
        break
    else:
        print("Can't understand what do you want. Please, try againg")