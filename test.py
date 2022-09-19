import scre
import re
import time
import tqdm
import random

TEST_NUM = 10000

def get_re_string():
    num = random.randint(5, 100)

    p = ""
    for i in range(num):
        p += chr(ord('a') + random.randint(0, 25))
    return p

re_string_list = [get_re_string() for i in range(TEST_NUM)]


p = scre.compile(re_string_list[0])
start = time.time()
for i in range(TEST_NUM):
    ret = p.fullmatch(re_string_list[0])
end = time.time()
print(end - start)

p = re.compile(re_string_list[0])
start = time.time()
for i in range(TEST_NUM):
    ret = p.fullmatch(re_string_list[0])
end = time.time()
print(end - start)


start = time.time()
for i in range(TEST_NUM):
    p = scre.compile(re_string_list[i])
    ret = p.fullmatch(re_string_list[i])
end = time.time()
print(end - start)

start = time.time()
for i in range(TEST_NUM):
    p = re.compile(re_string_list[i])
    ret = p.fullmatch(re_string_list[i])
end = time.time()
print(end - start)