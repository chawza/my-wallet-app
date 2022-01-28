from Crypto.PublicKey import RSA

rsa_public_key = 'rsa_public.pem'
rsa_private_key = 'rsa_private.pem'

key = RSA.generate(bits=2048)
private_key = key.exportKey()
with open(rsa_private_key, 'wb') as file:
    file.write(private_key)

public_key = key.public_key()
public_key = public_key.exportKey()
with open(rsa_public_key, 'wb') as file:
    file.write(public_key)
