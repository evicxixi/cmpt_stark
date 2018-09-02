from urllib.parse import urlencode

info = {'k1':'v1','k2':'v2','k3':'v3'}

v = urlencode(info)
print(v)