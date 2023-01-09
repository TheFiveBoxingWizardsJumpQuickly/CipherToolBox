#https://tex2e.github.io/blog/crypto/modular-mul-inverse
def xgcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modinv(a, m):
    g, x, y = xgcd(a, m)
    if g != 1:
        return 0
    else:
        return x % m

def rsa_encode(m, e, n):
    return pow(m, e, n)

#IF n = p * q
def rsa_decode(c, e, n, p, q):
    d = modinv(e, (p-1) * (q-1))
    return [pow(c, d, n),d]

'''
def __main__():
    n= 1507174481318465466523128991270360113716039108832684797969162807571085936787014823053726763818939
    c= 53286690260644388097425675112080667172813335026633897835642198108382149310515357443327652099643
    p= 1109726393111220267897048234180020381849194524413
    q= 1358149621991924365919728441827592260914436698903
    e= 104547
'''    
