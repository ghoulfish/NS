#!/usr/local/bin/python3
import binascii
import wave

#########################
####### RC4 #############
#########################


def ksa(key_b):
    ''' KSA - Key-scheduling algorithm (KSA)
    '''
    k = bytearray(range(256))
    j = 0
    for i in range(256):
        j = (j + k[i] + key_b[i % len(key_b)]) % 256
        k[i], k[j] = k[j], k[i]
    return bytes(k)


def prga(s):
    ''' PRGA - Pseudo-random generation algorithm
    '''
    s = bytearray(s)
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        yield s[(s[i] + s[j]) % 256]


def rc4(key_b, plaintext_b):
    ''' returns the RC4 ciphertext corresponding to the keys and plaintext
    given as bytes
    (bytes, bytes) -> bytes
    >>> rc4(b'Key',b'Plaintext')
    b'\xbb\xf3\x16\xe8\xd9@\xaf\n\xd3'
    '''
    ciphertext_b = bytearray()
    random = prga(ksa(key_b))
    for byte in plaintext_b:
        ciphertext_b.append(byte ^ next(random))
    return bytes(ciphertext_b)


#########################
####### utils ###########
#########################


def utf82bytes(s):
    ''' returns the bytes encoding of utf-8 string s given as argument
    (string) -> bytes
    >>> utf82ba('Key')
    b'Key'
    '''
    return s.encode('utf-8')


def bytes2utf8(b):
    ''' returns the utf-8 string of the bytes ba given as parameter
    (bytes) -> string
    >>> ba2utf8(b'Key')
    'Key'
    '''
    return b.decode('utf-8')


def armor2bytes(a):
    ''' returns the bytes of the ASCII armor string a given as parameter
    (string)-> bytes
    >>> armor2ba('S2V5')
    b'Key'
    '''
    return binascii.a2b_base64(a)


def bytes2armor(b):
    ''' returns the ASCII armor string of the bytes ba given as parameter
    (bytes)-> string
     >>> ba2armor(b'Key')
    'S2V5'
    '''
    return bytes2utf8(binascii.b2a_base64(b))

#########################
### textfile support ####
#########################


def rc4_textfile_encrypt(key, input_filename, output_filename):
    ''' encrypts the input plaintext file into the ASCI-armored output file
    using the key
    (string, string, string) -> None
    '''
    key_b = utf82bytes(key)
    input_file = open(input_filename, "r")
    plaintext_b = utf82bytes(input_file.read())
    input_file.close()
    ciphertext_b = rc4(key_b, plaintext_b)
    output_file = open(output_filename, "w")
    output_file.write(bytes2armor(ciphertext_b))
    output_file.close()


def rc4_textfile_decrypt(key, input_filename, output_filename):
    ''' decrypts the ASCII-armored input file to the plaintext output file
    using the key
    (string, string, string) -> None
    '''
    key_b = utf82bytes(key)
    input_file = open(input_filename, "r")
    ciphertext_b = armor2bytes(input_file.read())
    input_file.close()
    plaintext_b = rc4(key_b, ciphertext_b)
    output_file = open(output_filename, "w")
    output_file.write(bytes2utf8(plaintext_b))
    output_file.close()

#########################
### binary support ######
#########################


def rc4_binary(key, input_filename, output_filename):
    ''' encrypts/decrypts the binary input file to the binary output file file
    using the key
    (string, string, string) -> None
    '''
    key_b = utf82bytes(key)
    input_file = open(input_filename, "rb")
    ciphertext_b = input_file.read()
    input_file.close()
    plaintext_b = rc4(key_b, ciphertext_b)
    output_file = open(output_filename, "wb")
    output_file.write(plaintext_b)
    output_file.close()

#########################
### wave support ########
#########################


def rc4_wave(key, input_filename, output_filename):
    ''' encrypts/decrypts the wave input file to the wave output file file
    using the key
    (string, string, string) -> None
    '''
    key_b = utf82bytes(key)
    input_file = wave.open(input_filename, "rb")
    ciphertext_b = input_file.readframes(input_file.getnframes())
    input_header = input_file.getparams()
    input_file.close()
    plaintext_b = rc4(key_b, ciphertext_b)
    output_file = wave.open(output_filename, "wb")
    output_file.setparams(input_header)
    output_file.writeframes(plaintext_b)
    output_file.close()

#########################
### tests  ##############
#########################


if __name__ == '__main__':
    ''' Tests
    '''
    # Works with Python 3
    # Declare a value of type Bytes
    plaintext_b = b'Plaintext'
    # iterate throught a bytes value
    for byte in plaintext_b:
        print(byte)
    # modify a byte does not work because Bytes are immutable
    # the following line raises an exception
    # plaintext_b[0],plaintext_b[-1] = plaintext_b[-1],plaintext_b[0]
    # so we need to convert it into a mutable bytearray
    plaintext_ba = bytearray(plaintext_b)
    plaintext_ba[0], plaintext_ba[-1] = plaintext_ba[-1], plaintext_ba[0]
    # and convert it back to byte
    plaintext_b = bytes(plaintext_ba)
    print(plaintext_b)
    # making a xor byte per byte
    key_b = b'Secretext'
    cipher_b = bytearray(b'')
    for i in range(len(plaintext_b)):
        print(i)
        cipher_b.append(plaintext_b[i] ^ key_b[i])
    print(bytes(cipher_b))
    print("-----------------------------------")

    # basic function test
    print(rc4(b'Key', b'Plaintext') == b'\xbb\xf3\x16\xe8\xd9@\xaf\n\xd3')
    print(utf82bytes('Key') == b'Key')
    print(bytes2utf8(b'Key') == 'Key')
    print(armor2bytes('S2V5') == b'Key')
    print(bytes2armor(b'Key') == 'S2V5\n')
    print("-----------------------------------")

    # i/o file test
    # import filecmp

    # rc4_textfile_encrypt("Key", "test/neil.txt", "test/ct.asc")
    # rc4_textfile_decrypt("Key", "test/neil.asc", "test/pt.txt")
    # print(filecmp.cmp("test/neil.asc", "test/ct.asc"))
    # print(filecmp.cmp("test/neil.txt", "test/pt.txt"))

    # rc4_binary("Key", "test/neil.jpg", "test/cb.bin")
    # rc4_binary("Key", "test/neil.bin", "test/pb.jpg")
    # print(filecmp.cmp("test/neil.bin", "test/cb.bin"))
    # print(filecmp.cmp("test/neil.jpg", "test/pb.jpg"))

    # rc4_wave("Key", "test/neilc.wav", "test/pw.wav")
