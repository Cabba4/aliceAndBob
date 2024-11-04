m1 = '4C49464549534C494B4541424F584F4643484F434F4C41544553'
c1 = '1E19041F1905140106111815090A15140C050017001919061C14'



m1_bytes = bytes.fromhex(m1)
c1_bytes = bytes.fromhex(c1)

k1 = bytes([m ^ c for m,c in zip(m1_bytes, c1_bytes)])
print(k1.hex())

c2 = '0B1F171415001D1A061A1600111A1B0616021A03061914151C13'
c2_bytes = bytes.fromhex(c2)
m2_bytes = bytes([k ^ c for k,c in zip(k1, c2_bytes)])

print("M2 hex is: ", m2_bytes.hex())
print("M2 ascii is: ", m2_bytes.decode('ascii') )