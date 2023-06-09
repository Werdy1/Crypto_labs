import random
import time
from math import sqrt, exp, log2, ceil, floor

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

def legendre_symbol (a: int,p: int):
    # a - some integer; p - prime number
    # I will count Legendre symbol using Euler's criterion
    power = (p - 1)//2
    if power > 1000:
        result = horners_method(a, power, p)
    else:
        result = (a**power)%p
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

def get_power_vector(n: int, base: list):
    # returns vector of powers from base of the expansion of a number n in mod 2
    counter = len(base)
    vector = [0] * counter
    i = 0
    if base[0] == -1:
        if n < 0:
            vector[0] = 1
            n = n//-1
        i += 1
    while n!=1 and i < counter:
        if n % base[i] == 0: 
            n = n//base[i]
            vector[i] = vector[i]^1
        else:
            i+=1
    if n!=1:
        #print("Oops, there is no such number in the base. Too bad!")
        pass
    return vector

def gauss_method(matrix: list):
    # must receive the matrix (2d list)
    # return all possible combination that result in 0-vector
    # answer is 2d array
    answer = []
    height = len(matrix)
    width = len(matrix[0])
    marked_rows = [0] * width
    is_unmarked_rows = [1] * height
    # matrix simplification
    for j in range(width):
        for i in range(height):
            if matrix[i][j] == 1:
                marked_rows[j] = i
                is_unmarked_rows[i] = 0
                for y in range(width):
                    if y == j:
                        continue
                    if matrix[i][y] == 1:
                        for x in range(height):
                            matrix[x][y] = matrix[x][y] ^ matrix[x][j]
                break
    # Finding result vectors
    for i in range(height):
        if is_unmarked_rows[i]:
            temp = [i]
            check = 0
            for j in range(width):
                if matrix[i][j]:
                    temp.append(marked_rows[j])
                    check = 1
            if check:
                answer.append(temp)
    return answer

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

def method_of_trial_divisions(n: int, some_prime_numbers: list = []):
    # n - integer to factorize; 
    # Since all numbers could be represented in bit, my B will be 2
    answer = [n] # list where found dividers and new n will be stored
                 # if none dividers found list with only n will be returned
    if n ==1:
        print("Number equals 1")
        return answer
    if miller_rabin_probability_test(n):
        print("Already prime")
        return answer
    if some_prime_numbers == []:
        some_prime_numbers = sieve_of_eratosthenes(n)
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

def brillhart_morrison_method(n: int):
    # this function will find one divider and after that ends
    answer = [n] # list where found dividers and new n will be stored
                 # if none dividers found list with only n will be returned
    if n ==1:
        print("Number equals 1")
        return answer
    if miller_rabin_probability_test(n):
        print("Already prime")
        return answer
    a = 1/sqrt(2)
    L = exp(sqrt(log2(n)*log2(log2(n))))
    end = ceil(L**a)
    prime_numbers = sieve_of_eratosthenes(end)
    factorial_base = [-1]
    for number in prime_numbers:
        if legendre_symbol(n,number) == 1:
            factorial_base.append(number)
    k = len(factorial_base)
    chain_fraction = [0] * (k+1)
    V = 1
    a = floor((sqrt(n)))
    chain_fraction[0] = a
    U = a
    for i in range(k + 1):
        V = (n - U**2)//V
        a = floor((sqrt(n)+U)/V)
        chain_fraction[i] = a
        U = a * V - U
    b = [0] * (k+3)
    b[1] = 1
    b_squares = [0]*(k+1)
    for i in range(2, k + 3):
        b[i] = (b[i-1]*chain_fraction[i-2]+b[i-2])%n
        b_squares[i - 2] = (b[i]**2)%n
    matrix = [[]] * (k + 1)
    for i in range(k + 1):
        matrix[i] = get_power_vector(b_squares[i],factorial_base)   
    vectors_combinations = gauss_method(matrix) 
    check = 1
    for combination in vectors_combinations:
        X = 1
        Y = 1
        for number in combination:
            X = (X * b[number + 2])%n
            Y = (Y * b_squares[number])%n
        Y = int(sqrt(Y))
        if X != Y and X != n - Y:
            poss_divider  = gcd(X+Y,n)
            if poss_divider == 1:
                poss_divider  = gcd(X-Y,n)
            if poss_divider != 1:
                n = n//poss_divider
                answer[0] = n
                answer.append(poss_divider)
                check = 0
                break
    if check:
        print(f"Sorry, can't find any solution")
    return answer
while 1:
    print("Welcome, please choose what algorithm you want to use\n"\
          "1 - miller_rabin_probability_test\n"\
          "2 - method_of_trial_divisions\n"\
          "3 - pollards_p_method\n"\
          "4 - brillhart_morrison_method\n"\
          "5 - Optimal (all at once)\n"\
          "0 - Exit"\
          )
    n = input()
    if n == "1":
        number = int(input("Please, enter your number:"))
        start = time.time()
        result = miller_rabin_probability_test(number)
        end = time.time()
        print("Prime number" if result else "Not a prime number")
        print("It takes:",end - start,"seconds")
    elif n == "2":
        number = int(input("Please, enter your number:"))
        start = time.time()
        result = method_of_trial_divisions(number)
        end = time.time()
        print(result)
        print("It takes:",end - start,"seconds")
    elif n == "3":
        number = int(input("Please, enter your number:"))
        start = time.time()
        result = pollards_p_method(number)
        end = time.time()
        print(result)
        print("It takes:",end - start,"seconds")
    elif n == "4":
        number = int(input("Please, enter your number:"))
        start = time.time()
        result = brillhart_morrison_method(number)
        end = time.time()
        print(result)
        print("It takes:",end - start,"seconds")
    elif n == "5":
        result = []
        number = int(input("Please, enter your number:"))
        start = time.time()
        some_prime_numbers = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
        start_of_function = time.time()
        temp = method_of_trial_divisions(number,some_prime_numbers)
        end_of_function = time.time()
        result = result + temp[1:]
        print("Method of trial divisions:",temp)
        print(end_of_function-start_of_function,"seconds")
        number = temp[0]
        start_of_function = time.time()
        temp = pollards_p_method(number)
        end_of_function = time.time()
        result = result + temp[1:]
        print("Pollards p method",temp)
        print(end_of_function-start_of_function,"seconds")
        
        while number != temp[0]:
            number = temp[0]
            start_of_function = time.time()
            temp = brillhart_morrison_method(number)
            end_of_function = time.time()
            result = result + temp[1:]
            if len(temp) > 1:
                print("Brillhart-Morrison method:",temp)
            print(end_of_function-start_of_function,"seconds")
        result += temp
        end = time.time()
        print("All it takes:",end - start,"seconds")
        print(result)
    elif n == "0":
        break
    else:
        print("Can't understand what do you want. Please, try againg")