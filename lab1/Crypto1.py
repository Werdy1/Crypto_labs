import random
def gcd(a,b):
    return abs(a) if b==0 else gcd(b, a%b)

def find_highest_power_of_two(n):
    # find the max 2**s that can divide number (n)
    return (n & (~(n - 1)))

def miller_rabin_probability_test(n): # works fine for 7 digits, on 8 digits rapid increase in time
    # if number(n) is prime the function will return True
    # otherwise False
    power_of_two = find_highest_power_of_two(n-1)
    s = power_of_two.bit_length()
    d = int((n-1)/power_of_two) #for whatever reason it's not working with double, so converted to int (maybe somethig with) double representation
    k = 5
    for i in range(k):
        x = random.randint(2,n-1) # both ends includes
        if gcd(n,x) > 1:
            return False
        base = (x**d)%n 
        if  base == 1 or base == (n - 1):
            continue
        for j in range(1,s):
            base = (base**2)%n
            if base == n - 1:
                break
            elif base == 1 or j == s-1:
                return False
    return True      

def method_of_trial_divisions(n):
    pass

def pollards_p_method(n):
    pass

def brillhart_morrison_method(n):
    pass

number = int(input("Please enter your number:"))
print(miller_rabin_probability_test(number))