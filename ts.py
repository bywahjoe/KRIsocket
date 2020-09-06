import os

ok=os.stat('kompaslog.txt').st_size>0
print(ok)