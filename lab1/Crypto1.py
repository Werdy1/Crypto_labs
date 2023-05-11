
def gcd(a,b):
    return abs(a) if b==0 else gcd(b, a%b)

def find_highest_power_of_two(n):
    return (n & (~(n - 1)))

def method_of_trial_divisions(n):
    pass

def pollards_p_method(n):
    pass

def brillhart_morrison_method(n):
    pass

number = int(input("Please enter your number:"))