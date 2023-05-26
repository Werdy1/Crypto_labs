import random
from math import ceil,sqrt
import threading

def gcd(a: int,b: int):
    return abs(a) if b==0 else gcd(b, a%b)

def find_highest_power_of_two(n: int):
    # find the max 2**s that can divide number (n)
    return (n & (~(n - 1)))

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

def sieve_of_eratosthenes(n: int):
    # return prime number within range [2,n]
    result = []
    is_prime = [1]*(n+1)
    is_prime[0], is_prime[1] = 0 , 0
    for i in range(2,ceil(sqrt(n))):
        if is_prime[i]:
            j = i * i
            while j < n + 1:
                is_prime[j] = 0
                j += i
    for i in range(2,n+1):
        if is_prime[i]:
            result.append(i)
    return result

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

def method_of_trial_divisions(n: int):
    # n - integer to factorize; 
    # Since all numbers could be represented in bit, my B will be 2
    answer = [n] # list where found dividers and new n will be stored
                 # if none dividers found list with only n will be returned
    if n < 2:
        return answer
    if miller_rabin_probability_test(n):
        return answer
    some_prime_numbers = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
    while n != 1:
        check = 1 # variable for checking if any prime number was found, to avoid infinite loop
        t = n.bit_length()
        representation = (bin(n)[:1:-1])
        for poss_divider in some_prime_numbers:
            r = 1
            result = 0
            for i in range(t):
                result = (result + int(representation[i]) * r) % poss_divider
                r = (r * 2) % poss_divider
            if result == 0:
                n = n//poss_divider # Changed for floor division, because normal division return double which cause problems
                answer[0] = n
                answer.append(poss_divider)
                check = 0
                break
        if check:
            break  
    return answer

def pollards_p_method(n: int): 
    # this function will find one divider and after that ends
    # I will use classic function: f(x) = x^2 + 1
    answer = [n] # list where found dividers and new n will be stored
                 # if none dividers found list with only n will be returned 

    if n < 2:
        return answer
    if miller_rabin_probability_test(n):
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

def find_canonical_form(n: int): # uses method of trial divisions and pollards p method
    # return canonical form
    dividers = method_of_trial_divisions(n)
    if len(dividers) < 2:
        return dividers
    temp = dividers[0]
    canonical_form = dividers[1:] 
    while temp != 1:
        dividers = pollards_p_method(temp)
        temp = dividers[0]
        if len(dividers)>1:
            canonical_form.append(dividers[1])
        else:
            canonical_form.append(dividers[0])
            break
    return canonical_form

def find_field_generator(p: int):
    # p - prime number;
    n = p - 1
    unique_canonic_form = set(find_canonical_form(n))
    answer = 0 
    for i in range(2,p):
        check = 1 # check for possible generator
        for number in unique_canonic_form:
            if (i**(n//(number)))%p == 1:
                check = 0
                break
        if check:
            answer = i
            break
    return answer


def generate_equation(order: int):
    prime_numbers = sieve_of_eratosthenes(10**order)
    min_element = 10**(order - 1)
    for i in range(len(prime_numbers)):
        if prime_numbers[i] > min_element:
            prime_numbers = prime_numbers[i:]
            break
    prime = random.choice(prime_numbers)
    generator = find_field_generator(prime)
    power = random.randint(2, prime - 2)

    b = (generator**power)%prime
    return [generator,power,b,prime]

while 1:
    print("Welcome, please enter 1 when you are ready\n"\
          "1 - generate the equation\n"\
          "0 - Exit"\
          )
    n = input()
    if n == "1":
        order = int(input("Please, enter your p number (prime number) order :"))
        generator,power,b,prime = 0,0,0,0 

        def wait_for_generating(order):
            global generator,power,b,prime
            generator,power,b,prime = generate_equation(order)

        input_thread = threading.Thread(target=wait_for_generating, args=[order]) 
        input_thread.start()                                                       
        input_thread.join(timeout=600)
        if input_thread.is_alive():
            print("Timer expired. Sorry this is program limit")
            continue
        print(f"Solve it if you dare: {generator}^x = {b} mod {prime}")
        answer = 0

        def wait_for_input():
            global answer
            answer = int(input("Your answer: "))

        input_thread = threading.Thread(target=wait_for_input)
        input_thread.start()
        input_thread.join(timeout=300)
        if input_thread.is_alive():
            print("\nTimer expired. Sorry you gotta be faster")
        else:
            if answer == power:
                print("Congratulations!")
            else:
                print(f"Wrong, the right answer was {power}")
    elif n == "0":
        break
    else:
        print("Can't understand what do you want. Please, try againg")
