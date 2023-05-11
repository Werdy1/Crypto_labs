import random
def gcd(a: int,b: int):
    return abs(a) if b==0 else gcd(b, a%b)

def find_highest_power_of_two(n: int):
    # find the max 2**s that can divide number (n)
    return (n & (~(n - 1)))

def miller_rabin_probability_test(n: int): # works fine for 7 digits, on 8 digits rapid increase in time (1!)
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
        base = (x**d)%n # (1!) the problem is here //? algorithm for big powers 
        if  base == 1 or base == (n - 1):
            continue
        for j in range(1,s):
            base = (base**2)%n
            if base == n - 1:
                break
            elif base == 1 or j == s-1:
                return False
    return True      

def method_of_trial_divisions(n: int):
    # Since all numbers could be represented in bit, my B will be 2
    answer = [] # list where found dividers will be stored
                # if none dividers found empty list will be returned
    some_prime_numbers = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
    while n != 1:
        check = 1 # variable for checking if any prime nummber was found, to avoid infinite loop
        t = n.bit_length()
        representation = (bin(n)[:1:-1])
        for poss_divider in some_prime_numbers:
            r = 1
            result = 0
            for i in range(t):
                result = (result + int(representation[i]) * r) % poss_divider
                r = (r * 2) % poss_divider
            if result == 0:
                n = int(n/poss_divider) 
                answer.append(poss_divider)
                check = 0
                break
        if check:
            break
    return answer

def pollards_p_method(n: int):
    pass

def brillhart_morrison_method(n: int):
    pass

number = int(input("Please, enter your number:"))
print(method_of_trial_divisions(number))
