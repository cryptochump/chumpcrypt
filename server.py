from flask import Flask, request
import json
from random import randint

app = Flask(__name__)

secret = 'This is the secret'

kb = [ord(x) for x in secret]
def chump_encrypt_byte(p, M) :
    c = 0       # ciphertext output value
    pi = 1      # p^i
    for i,ki in zip(range(len(secret)),kb) :
        c = (c + pi * ki) % M
        pi *= p
    return c

def chump_encrypt(data, headers) :
    M = random_modulus()
    ciphertext = [chump_encrypt_byte(x, M) for x in data]
    headers['X-Cipher-Modulus'] = str(M)
    return json.dumps(ciphertext)

@app.route('/', defaults={'path': ''}, methods = ['POST', 'GET'])
@app.route('/<path:path>', methods = ['POST', 'GET'])
def encrypt(path):
    headers = {'Server' : 'ChumpCrypt-Server/1.0', 'Content-Type' : 'application/json'}
    try :
        data = request.get_data()
        if data is None :
            data = []
        data = json.loads(data)
        if isinstance(data, list) and all(isinstance(x, int) for x in data):
            return chump_encrypt(data, headers), 200, headers
    except :
        import sys
        print(sys.exc_info())
        pass
    return '\'Invalid plaintext array\'', 200, headers

def generate_primes(minval, maxval):
    comp = {}
    x = 2
    while x <= maxval:
        if x not in comp:
            if (x > minval) :
                yield x
            comp[x * x] = [x]
        else:
            for p in comp[x]:
                comp.setdefault(p + x, []).append(p)
            del comp[x]
        x += 1

moduli = list(generate_primes(256, 65536))
def random_modulus() :
    return moduli[randint(0, len(moduli) - 1)]

app.run()