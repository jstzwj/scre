import scre
p = scre.compile("abc|aaa")
ret = p.fullmatch("aaa")
print(ret)
