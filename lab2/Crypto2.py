import random

def gcd(a: int,b: int):
    return abs(a) if b==0 else gcd(b, a%b)

def find_highest_power_of_two(n: int):
    # find the max 2**s that can divide number (n)
    return (n & (~(n - 1)))

def miller_rabin_probability_test(n: int): 
    # if number(n) is prime the function will return True
    # otherwise False
    if n==2:
        return True
    power_of_two = find_highest_power_of_two(n-1)
    s = power_of_two.bit_length()
    d = int((n-1)/power_of_two) #for whatever reason it's not working with double, so converted to int (maybe somethig with) double representation
    k = 5
    for i in range(k):
        x = random.randint(2,n-1) # both ends includes
        if gcd(n,x) > 1:
            return False
        base = horners_method(x,d,n)
        if  base == 1 or base == (n - 1):
            continue
        for j in range(1,s):
            base = (base**2)%n
            if base == n - 1:
                break
            elif base == 1 or j == s-1:
                return False
    return True

def pollards_p_method(n: int): 
    # this function will find one divider and after that ends
    # I will use classic function: f(x) = x^2 + 1
    answer = [n] # list where found dividers and new n will be stored
                 # if none dividers found list with only n will be returned 

    if n ==1:
        print("Number equals 1")
        return answer
    if miller_rabin_probability_test(n):
        print("Already prime")
        return answer
    x = 2
    y = 2
    poss_divider = 1
    while poss_divider == 1:
        x = (x**2 + 1) % n
        y = (y**4 + 2*(y**2) + 2) % n
        poss_divider = gcd(y-x,n)
    n = n//poss_divider
    answer[0] = n
    answer.append(poss_divider)  
    return answer

def horners_method(x: int, d: int, n: int = 0): # used to calculate big powers of number (more than 4 digits)
    # x - base number; d - power of number; n - module (optional)
    representation = (bin(d)[2:])
    counter = d.bit_length()
    result = x
    for i in range(1, counter):
        result = (result**2)*(x**int(representation[i]))
        if n != 0:
            result = result % n 
    return result


def try_method(a: int, b:int,p: int):
    # where  a - base (generator); b - field element; p - module (prime number)
    # function returns power if finds one, or return -1
    answer = -1 
    n = p - 1 # order of the group
    for i in range(p-1): # I will int by int try every power until I find one or until the loop ends
        if i > 999:
            temp = horners_method(a,i,p) # for huge powers I will use horners method
        else:
            temp = (a**i)%p
        if temp == b:
            answer = i
            break
    return answer

def silver_polig_hellman(a: int, b:int,p: int):
    # where  a - base (generator); b - field element; p - module (prime number)
    n = p - 1 # order of the group
    temp = n
    canonical_form = []
    while temp != 1:
        numbers = pollards_p_method(n) # to do: add handling of infinite loop, if temp is prime?
        temp = numbers[0]
        canonical_form.append(temp[1])
    
    pass

n = int(input("Enter numbers:"))
print(try_method(2,13,37))
