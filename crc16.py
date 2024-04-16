import os
import random
import string
import sys


# 파일 생성 함수
def create_random_txt_files(num_files, file_size, output_dir):
    for i in range(num_files):
        filename = str(i) + ".txt"
        filepath = os.path.join(output_dir, filename)
        
        # 랜덤한 내용으로 파일 생성
        with open(filepath, 'w') as f:
            f.write(''.join(random.choices(string.ascii_letters + string.digits, k=file_size)))

# CRC-16 해시값 비교 함수
def compare_crc16_hashes(files_dir):
    #dict로 충돌
    crc16_hashes = {} 
    collided_files = []

    # 디렉토리 내의 모든 파일에 대해 CRC-16 해시값 계산
    for filename in os.listdir(files_dir):
        filepath = os.path.join(files_dir, filename)
        crc16_hash = calculate_crc16(filepath)

        # 해시값이 충돌하는 경우
        if crc16_hash in crc16_hashes:
            collided_files.append((filename, crc16_hashes[crc16_hash]))
        else:
            crc16_hashes[crc16_hash] = filename

    return collided_files

# CRC-16 해시값 계산 함수
def calculate_crc16(filepath):
    crc16_func = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0, xorOut=0xFFFFFFFF)
    with open(filepath, 'rb') as f:
        data = f.read()
        crc16 = crc16_func(data)
    return format(crc16, 'x')

def main():
    if len(sys.argv) < 2:
        print("Usage: python crc16.py [directory_name_to_make_txt_files]")
        sys.exit(1)

    num_files = 1000  # 생성할 파일의 개수
    file_size = 1000  # 파일의 크기 (바이트)
    output_dir = sys.argv[1]  # 생성된 파일을 저장할 디렉토리

    # 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        print("There is same directory name")
        sys.exit(1)


    # 랜덤한 텍스트 파일 생성
    create_random_txt_files(num_files, file_size, output_dir)

    # CRC-16 해시값 비교하여 충돌 확인
    collided_files = compare_crc16_hashes(output_dir)

    
    print("CRC-16 해시 충돌이 발생한 파일들:")
    for file1, file2 in collided_files:
            print(file1+"와"+file2)
    print("실행 종료")

    
if __name__ == "__main__":
    main()