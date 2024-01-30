

def add_four(a,b,c,d):
    return a+b+c+d

add_preset = lambda x,y: add_four(x,y, 3, 14)

print(add_preset(1,2))

def spam():
    print('ham')

def gen_spam():
    return spam

print(gen_spam())
print(gen_spam()())



def minimul(x):
    return lambda y: x*y

mul = lambda x: lambda y: y*x

print(mul(4)(2))
print(minimul(4)(6))