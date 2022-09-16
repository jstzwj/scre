import scre
import re
import time

re_string = "abcdefghijklmn"

p = scre.compile(re_string)
start = time.time()
for i in range(100000):
    ret = scre.match(p, re_string)
end = time.time()
print(end - start)

p = re.compile(re_string)
start = time.time()
for i in range(100000):
    ret = re.match(p, re_string)
end = time.time()
print(end - start)


import random
re_string_list = ["abc", "abcd", "abcde"]

start = time.time()
for i in range(100000):
    p = scre.compile(random.choice(re_string_list))
    ret = scre.match(p, re_string)
end = time.time()
print(end - start)

start = time.time()
for i in range(100000):
    p = re.compile(random.choice(re_string_list))
    ret = re.match(p, re_string)
end = time.time()
print(end - start)