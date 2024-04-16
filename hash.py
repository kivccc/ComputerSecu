import hashlib
import zlib
import crcmod
import sys

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(1024)  # 1024 바이트씩 읽어서 처리
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def calculate_crc16(filepath):
    crc16_func = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0, xorOut=0xFFFFFFFF)
    with open(filepath, 'rb') as f:
        data = f.read()
        crc16 = crc16_func(data)
    return format(crc16, 'x')

def calculate_crc32(filepath):
    prev = 0
    with open(filepath, 'rb') as f:
        for eachLine in f:
            prev = zlib.crc32(eachLine, prev)
    return format(prev & 0xFFFFFFFF, 'x')

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py [sha256|crc16|crc32] [file_path]")
        sys.exit(1)

    option = sys.argv[1]
    filepath = sys.argv[2]

    if option == "sha256":
        print("SHA-256:", calculate_sha256(filepath))
    elif option == "crc16":
        print("CRC-16:", calculate_crc16(filepath))
    elif option == "crc32":
        print("CRC-32:", calculate_crc32(filepath))
    else:
        print("Invalid option. Please choose sha256, crc16, or crc32.")
        sys.exit(1)

if __name__ == "__main__":
    main()

