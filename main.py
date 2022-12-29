import random 
from random import randint
import math
from math import gcd
from flask import Flask, redirect, url_for, render_template, request



#uses extended euclidean algorithm to find certificate of correctedness
def eea(subpq, e):
    x = [1,0]
    eea_d = [0,1]
    quotient_list = [0,0]
    remainder_list = [subpq, e]

    while 0 not in remainder_list:
        quotient_list.append(((remainder_list[-2]) // remainder_list[-1]))
        remainder_list.append((remainder_list[-2] - (remainder_list[-1] * quotient_list[-1])))
        x.append(  ( x[-2] - (x[-1] * quotient_list[-1]))  )
        eea_d.append(  ( eea_d[-2]) - (eea_d[-1] * quotient_list[-1])  )

        if ((e * eea_d[-1]) + (subpq * x[-1])) == 1:
            d = eea_d[-1]
            return d
            break

#solves congruence in simplified form 
def congruence(m, e, n):
   c = ((m**e)%n)
   return c


#converts string of length two into an ascii version via polynomail of 128
def word_num(message):
    #encoding via modulo 128 strategy
    temp_msg = ord(message[0]) + ord(message[1]) * 128
    return temp_msg



#takes in special polynomial and converts it back to characters
def num_word(mod_128):
    first = chr(mod_128 % 128)
    second = chr(mod_128//128)
    return first + second

#converts a list into a string where each element is seperated by a space
def spacer(los):
    space_string = ""
    for n in range(0,len(los)):
        if n == len(los) - 1:
            space_string += str(los[n])
            break
        else:
            space_string += str(los[n]) + ' '
    return space_string

    
#uses flt to find large prime numbers
def prime_generator():
    #p = randint(905071, 100000000)
    p = randint(563, 1000)
    a = 4
    
    while (a/p).is_integer() or not (a** (p - 1))%p == 1%p:
        #p = randint(905071, 100000000)
        p = randint(2, 1000)
        if not (a/p).is_integer() and (a** (p - 1))%p == 1%p and p not in [561, 1105, 1729, 2465, 2821, 
        6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361]:
            return p
            break

    if not (a/p).is_integer() and (a** (p - 1))%p == 1%p:
        return p



#does all the initial tasks of rsa
#generates e value
#generates d value
#generates private and public key 
def rsa_setup(p, q):
    subpq = ((p - 1) * (q - 1))
    n = (p * q)
    e_candidate = 0
    d = 0

    #loop to ensure a valid e value is choosen
    while math.gcd(e_candidate, subpq) != 1 or d < 0:
        e_candidate = randint(2, subpq)
        d = eea(subpq, e_candidate)

        if  math.gcd(e_candidate, subpq) == 1 and e_candidate < subpq and eea(subpq, e_candidate) > 1:
            #valid e value is assigned
            e = e_candidate
            #applies extend euclidean algorithm on
            # subpqx + ed = 1 and solves for d
            d = eea(subpq, e)
            break  

    #    d cannot be negative
    if  d < 1:
        return d

    #ensures positive d
    #generates all data needed in setup
    if d > 1:
        public_key = (e,n)
        private_key = (d,n)
        primes = (p, q)

        return [p, q, subpq, e, n, d]



#takes in a message of any length
#breaks it apart into submessages of length 2
#encrypts each message of sublength two
def rsa_encrypt(message):
    def encrypt_congruence(m, e, n):
        return congruence(m, e, n)
    
    p = prime_generator()
    q = prime_generator()
    info = rsa_setup(p, q)
    info.append(message)
    full_encrypt = []

    while not len(message) == 0:
    
        if len(message) == 1:
            full_encrypt.append(encrypt_congruence(ord(message), info[3], info[4]))
            message = ""
        else:
            full_encrypt.append(encrypt_congruence(word_num(message[:2]), info[3], info[4]))
            message = message[2:]
        if len(message) == 0:
            info.append(full_encrypt)
            return info


#decrypts ciphertext
def rsa_decrypt(cipher, d_val, n_val):
    def decrypt_congruence(C, d, n):
        return congruence(C, d, n)
    
    
    full_decrypt = ""

    for i in range (0,len(cipher)):
        full_decrypt += num_word(decrypt_congruence(int(cipher[i]), d_val, n_val))
    
    return full_decrypt



#Allows user to encrypt and decrypt information
def customer_encrypt():
    message = input("What message would you like to encrypt? ")
    encrypted = rsa_encrypt(message)
    print("Great! You're encrypted message is " + spacer(encrypted[-1]))
    print("You're d value is " + str(encrypted[5]))
    print("You're n value is " + str(encrypted[4]))
    print("Psst I would keep those a secret!")

    decrypt = input("Would like to decrpyt a message?(yes/no)")
    if decrypt == 'yes' or 'y' or 'Yes' or 'YES' or 'yES' or 'yEs':
        cipher = input("Please type the message you would like to decrypt:")
        cipher = cipher.split()
        d = int(input("Please type your d value:"))
        n = int(input("Please type your n value:"))
        print('loading.......')
        print("Congratulations your original message was " + rsa_decrypt(cipher, d, n))
    elif decrypt == 'no' or 'n' or 'No':
        print("Thank you, have a nice day!")
    else:
        print("Not an option")


app = Flask(__name__)

@app.route("/start", methods=["POST", "GET"])
def start():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST", "GET"])     
def encrypt():
    message = request.form.get("message")
    if message is None: 
        info = [0,0,0,0,0,0, "  "]
        return render_template("encrypt.html", 
                code=spacer(info[-1]), 
                    d_val = info[5], n_val = info[4])
    else:
        info = rsa_encrypt(message)
        return render_template("encrypt.html", 
                code=spacer(info[-1]), 
                    d_val = info[5], n_val = info[4])
        
      

@app.route("/decrypt", methods=["POST", "GET"])
def decrypt():
    C = request.args.get("C")
    d = request.args.get('d')
    n = request.args.get('n')
    if C is None or d is None or n is None:
        C = 1
        d = 1
        n = 1
        return render_template("decrypt.html", decrypted_message = "Sorry atleast one input is incorrect")

    elif rsa_decrypt(str(C).split(),int(d),int(n)) is None:
        return render_template("decrypt.html", decrypted_message = "Sorry atleast one input is incorrect")

    else:
        for x in str(C).split():
            if int(x) >= int(n):
                return render_template("decrypt.html", decrypted_message = "Sorry atleast one input is incorrect :(")


        return render_template("decrypt.html", decrypted_message = rsa_decrypt(str(C).split(),int(d),int(n)))
        
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)






 