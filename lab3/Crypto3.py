import time
import random
from math import exp, log10, sqrt, ceil, floor
import numpy as np

def gcd(a: int,b: int):
    return abs(a) if b==0 else gcd(b, a%b)

def find_highest_power_of_two(n: int):
    # find the max 2**s that can divide number (n)
    return (n & (~(n - 1)))

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
        base = pow(x,d,n)
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
    # n - positive integer to factorize; 
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

def get_power_vector(alpha: int, base: list):
    # will return power vector of a number, otherwise empty list
    # uses custom base to make a vector
    # for proper functioning requires a sorted list
    base_len = len(base)
    power_vector = [0] * base_len
    canonical_form = find_canonical_form(alpha)
    for number in canonical_form:
        check = 0 # check for snooth number; 0 - smooth, 1 - not smooth
        for i in range(base_len):
            if number == base[i]:
                power_vector[i] += 1
                break
            elif i == (base_len - 1): # happens only if alpha is not smooth
                check = 1
                break
        if check:
            power_vector = []
            break
    return power_vector

def gaussian_elimination(matrix: list, width: int, height: int):
    # must receive the matrix (2d list)
    # answer is 2d array; pairs (variable, value)
    # time complexity O(n^3), where n is number of unknown variables
    result = [0]*width
    pivot_row = 0
    pivot_column = 0
    pivot_coords = []
    while pivot_row < height and pivot_column < width: # forward direction
        row = -1
        for i in range(pivot_row, height):
            if matrix[i][pivot_column] != 0:   # find the pivot_row
                row = i
                break
        if row == -1:
            pivot_column += 1 # if no raw found, change the column
            continue
        matrix[row], matrix[pivot_row] = matrix[pivot_row], matrix[row] # swap the rows
        pivot_coords.append([pivot_row,pivot_column])
        for i in range(pivot_row + 1, height):
            coef = matrix[i][pivot_column] / matrix[pivot_row][pivot_column]
            matrix[i][pivot_column] = 0
            for j in range(pivot_column + 1, width + 1):
                matrix[i][j] -= matrix[pivot_row][j] * coef
        pivot_row += 1
        pivot_column += 1
    #for coords in pivot_coords[::-1]: # back direction
    #    row = coords[0]
    #    column = coords[1]
    #    matrix[row][width] /= matrix[row][column]
    #    matrix[row][column] = 1
    #    result[column] = matrix[row][width]
    #    for i in range(row):
    #        coef = matrix[i][column] / matrix[row][column]
    #        matrix[i][column] = 0
    #        matrix[i][width] -=  matrix[row][width]* coef
    return result

def is_linearly_independent(matrix, new_vector):
    if len(matrix) == 0:
        return True  # first vector
    else:
        new_matrix = np.vstack((matrix, new_vector))
        rank_original = np.linalg.matrix_rank(matrix)
        rank_new = np.linalg.matrix_rank(new_matrix)
        if rank_new > rank_original:
            return True  # vector is linearly independent
        else:
            return False

def index_calculus(a: int, b:int,p: int):
    # where  a - base (generator); b - field element; p - module (prime number)
    # function returns power if finds one, or return -1
    answer = -1 
    n = p - 1 # order of the group
    c = 3.38
    B = c * exp(0.5 * sqrt(log10(n) * log10(log10(n))))
    factorial_base = sieve_of_eratosthenes(floor(B))
    factorial_base.sort()
    factorial_base_len = len(factorial_base)
    enough_amount_of_vecotrs = factorial_base_len
    vectors = []
    vectos_values = []
    prev = 1
    amount_of_vectors = 0
    while enough_amount_of_vecotrs != amount_of_vectors:
        k = random.choice(range(1,n)) 
        alpha_k = (prev * a) % p
        vector = get_power_vector(alpha_k, factorial_base)
        prev = alpha_k
        if vector:
            if is_linearly_independent(vectors, vector):
                vectors.append(vector)
                vectos_values.append(k)
                amount_of_vectors += 1
    matrix_body = np.array(vectors)
    matrix_values = np.array(vectos_values)
    values = np.linalg.solve(matrix_body, matrix_values)
    while 1:
        l = random.choice(range(1,n))
        candidate = (b * pow(a,l,p))%p
        vector = get_power_vector(candidate, factorial_base)
        if vector:
            answer = 0
            for i in range(factorial_base_len):
                if vector[i] != 0:
                    answer += (vector[i] * (values[i] % n)) % n
            answer = (answer - l) % n
            break
    return answer

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
        print(index_calculus(a,b,p))
    elif n == "0":
        break
    else:
        print("Can't understand what do you want. Please, try againg")