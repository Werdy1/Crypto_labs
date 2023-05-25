import random

def gcd(a: int,b: int):
    return abs(a) if b==0 else gcd(b, a%b)

def find_highest_power_of_two(n: int):
    # find the max 2**s that can divide number (n)
    return (n & (~(n - 1)))

def find_inverted(n: int, p: int):
    q_list = [0,1]
    remainder = 0
    mod = p
    while remainder != 1:
        remainder = p%n
        q = (p-remainder)//n
        q_list.append(-q)
        p = n
        n = remainder
    for i in range(2,len(q_list)):
        q_list[i] = (q_list[i]*q_list[i-1] + q_list[i-2])%mod
    return q_list[-1]

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

def chinese_remainder_theorem(equations: list, n: int):
    # function returns power if finds one, or return 0
    answer = 0
    for equation in equations:
        second = (n//equation[1])
        answer += (equation[0]*second*(find_inverted(second,equation[1])))%n
    return answer%n

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

def find_canonical_form(n: int): # uses method of trial divisions and pollards p method
    # return canonical from
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

def silver_polig_hellman_method(a: int, b:int,p: int):
    # where  a - base (generator); b - field element; p - module (prime number)
    # function returns power if finds one, or return -1
    answer = -1 
    n = p - 1 # order of the group
    canonical_form = find_canonical_form(n)
    unique_canonical_form = set(canonical_form) # same canonical form, but where every number is unique
    powers_of_canonical_form = {value: canonical_form.count(value) for value in unique_canonical_form}
    equations = []
    for prime_number in unique_canonical_form:
        table = [0]*prime_number
        l = powers_of_canonical_form[prime_number]
        equation = [0,prime_number**l]
        for j in range(prime_number):
            power = (n*j)//prime_number
            if power > 999:
                table[j] = horners_method(a,power,p)
            else:
                table[j] = (a**power)%p
        # ******
        x_seq = [0]*(l+1)
        inverted_element = find_inverted(a,p)
        for j in range(1,l+1):
            power = n//(prime_number**j)
            coef = (inverted_element**(sum(x_seq[1:j])))%p
            temp = ((b*coef)**power)%p
            x_seq[j] = (table.index(temp))*(prime_number**(j-1))
        equation[0] = sum(x_seq)
        equations.append(equation)
    answer = chinese_remainder_theorem(equations,n)
    return answer

#n = int(input("Enter numbers:"))
print(silver_polig_hellman_method(3,13,211))
