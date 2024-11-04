from sympy import discrete_log

a = 14
b = 8
g = 7
p = 17

intermediate_alice = pow(g, a, p)
intermediate_bob = pow(g, b , p)
print(intermediate_alice)
print(intermediate_bob)

final = pow(g, a*b, p)
print(final)

## check if correct
shouldbe_final = pow(intermediate_bob, a, p)

shouldbe_final_bob = pow(intermediate_alice, b, p)

if final == shouldbe_final and final == shouldbe_final_bob:
    print("Correct key")
    
    
X = 3
Y = 10

a = discrete_log(p, X, g)
b = discrete_log(p, Y, g)
print(a ,b)

final = pow(g, a*b, p)
print(final)