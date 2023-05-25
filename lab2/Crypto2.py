def gcd(a: int,b: int):
    return abs(a) if b==0 else gcd(b, a%b)

def pollards_p_method(n: int):
    # this function will find one divider and after that ends
    # I will use classic function: f(x) = x^2 + 1
    answer = [n] # list where found dividers and new n will be stored
                 # if none dividers found list with only n will be returned 
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


def try_method(n: int, a: int, b:int):
    # where n - module; a - base; b - field element 
    pass

def silver_polig_hellman(n: int, a: int, b:int):
    # where n - module; a - base; b - field element 
    pass

n = int(input("Enter a number:"))
print(n)
