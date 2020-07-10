import sys
import hashlib
try:
    import pyfiglet
    print(pyfiglet.print_figlet('Hash Generator'))
except:

    pass

print('-'*30,end='')
print('Hash Generator',end='')
print('-'*30)
def main():
    while True:
        hash=input('enter the string you want to be hashed').strip(' ')
        while True:
            op=int(input("""enter the option you want
            '22' to change the string
                1.md5
                2.sha1
                3.sha224
                4.sha3_224
                5.sha256
                6.sha3_256
                7.sha384
                8.sha3_384
                9.sha512
                10.sha3_512
                11.blake2b
                12.blake2s
                
            press '99' for exit """))
            def mdfive(hash):
                print('md5 hash: '+hashlib.md5(hash.encode('utf-8')).hexdigest())
            def shaone(hash):
                print('sha1 hash: '+hashlib.sha1(hash.encode('utf-8')).hexdigest())
            def shasix(hash):
                print('sha256 hash: '+hashlib.sha256(hash.encode('utf-8')).hexdigest())
            def sha3_224(hash):
                print('sha3_224 hash: '+hashlib.sha3_224(hash.encode('utf-8')).hexdigest())
            def sha384(hash):
                print('sha384 hash: '+hashlib.sha384(hash.encode('utf-8')).hexdigest())
            def sha3_384(hash):
                print('sha3_384 hash: '+hashlib.sha3_384(hash.encode('utf-8')).hexdigest())
            def sha256(hash):
                print('sha256 hash: '+hashlib.sha256(hash.encode('utf-8')).hexdigest())
            def sha3_256(hash):
                print('sha3_256 hash: '+hashlib.sha3_256(hash.encode('utf-8')).hexdigest())
            def sha512(hash):
                print('sha512 hash: '+hashlib.sha512(hash.encode('utf-8')).hexdigest())
            def sha3_512(hash):
                print('sha3_512 hash: '+hashlib.sha3_512(hash.encode('utf-8')).hexdigest())
            def blake1(hash):
                print('blake2b hash: '+hashlib.blake2b(hash.encode('utf-8')).hexdigest())
            def blake2(hash):
                print('blake2s hash: '+hashlib.blake2s(hash.encode('utf-8')).hexdigest())
            if op==22:
                break
            elif op ==1:
                mdfive(hash)
            elif op==2:
                shaone(hash)
            elif op ==3:
                sha224(hash)
            elif op==4:
                sha3_224(hash)
            elif op==5:
                sha256(hash)
            elif op==6:
                sha3_256(hash)
            elif op==7:
                sha384(hash)
            elif op==8:
                sha3_384(hash)
            elif op==9:
                sha512(hash)
            elif op==10:
                sha3_512(hash)
            elif op==11:
                blake1(hash)
            elif op==12:
                blake2(hash)
            elif op==99:
                sys.exit(0)
                            
main()
