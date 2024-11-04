import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from binascii import unhexlify

cranberry = "cranberry"
cola = "cola"

hashed_cranberry = hashlib.sha256(cranberry.encode('ascii')).hexdigest()
hashed_cola = hashlib.sha256(cola.encode('ascii')).hexdigest()

print(hashed_cranberry[:11])
print(hashed_cola[:11])

sse_keyword_numsearch = 0
sse_keyword_numfile = 1

Kw_cran = hashlib.sha256((cranberry + str(sse_keyword_numsearch)).encode('ascii')).hexdigest()
print(Kw_cran[:11])

csp_keywords_address_cran = hashlib.sha256((Kw_cran + str(sse_keyword_numfile)).encode('ascii')).hexdigest()
print(csp_keywords_address_cran[:11])

Kw_cola = hashlib.sha256((cola + str(sse_keyword_numsearch)).encode('ascii')).hexdigest()
print(Kw_cola[:11])

csp_keywords_address_cola = hashlib.sha256((Kw_cola + str(sse_keyword_numfile)).encode('ascii')).hexdigest()
print(csp_keywords_address_cola[:11])