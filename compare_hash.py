import os
import random
import string
import sys
import crcmod
import hashlib
import zlib

# 파일 생성 함수
def create_random_txt_files(num_files, file_size, output_dir):
    for i in range(int(num_files)):
        filename = str(i) + ".txt"
        filepath = os.path.join(output_dir, filename)
        
        # 랜덤한 내용으로 파일 생성
        with open(filepath, 'w') as f:
            f.write(''.join(random.choices(string.ascii_letters + string.digits, k=file_size)))

# 해시값 비교 함수
def compare_hashes(files_dir,option):
    #dict로 충돌
    hash_dict = {} 
    collided_files = []

    # 디렉토리 내의 모든 파일에 대해 해시값 계산
    for filename in os.listdir(files_dir):
        filepath = os.path.join(files_dir, filename)

        if option == "sha256":
            hash = calculate_sha256(filepath)
        elif option == "crc16":
            hash = calculate_crc16(filepath)
        elif option == "crc32":
            hash = calculate_crc32(filepath)
        else:
            print("Invalid option. Please choose sha256, crc16, or crc32.")
            sys.exit(1)

        
        # 해시값이 충돌하는 경우
        if hash in hash_dict:
            collided_files.append((filename, hash_dict[hash]))
        else:
            hash_dict[hash] = filename

    return collided_files


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
    if len(sys.argv) < 4:
        print("Usage: python compare_hash.py [sha256|crc16|crc32] [filenumbers] [directory_name_to_make_txt_files]")
        sys.exit(1)

    num_files = sys.argv[2]  # 생성할 파일의 개수
    file_size = 1000  # 파일의 크기 (바이트)
    option = sys.argv[1]
    filepath = sys.argv[3]

    os.makedirs(filepath)

    # 랜덤한 텍스트 파일 생성
    create_random_txt_files(num_files, file_size, filepath)

    collided_files = compare_hashes(filepath,option)

    
    print("해시 충돌이 발생한 파일들:")
    for file1, file2 in collided_files:
            print(file1+ "와 "+file2)
    print("실행 종료")

    
if __name__ == "__main__":
    main()
