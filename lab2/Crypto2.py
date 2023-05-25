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
    pass

n = int(input("Enter numbers:"))
print(try_method(5,11,73))
