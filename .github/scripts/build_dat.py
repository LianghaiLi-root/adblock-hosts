#!/usr/bin/env python3
# Portable Lhl.dat (v2ray geosite protobuf) builder for GitHub Actions
# Input : domain/blacklist.txt, domain/whitelist.txt
# Output: geodata/Lhl.dat
import os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BL = os.path.join(ROOT, 'domain', 'blacklist.txt')
WL = os.path.join(ROOT, 'domain', 'whitelist.txt')
OUT = os.path.join(ROOT, 'geodata', 'Lhl.dat')

def clean(path):
    out=[]
    for ln in open(path, encoding='utf-8'):
        ln=ln.rstrip('\r\n')
        if not ln or ln.startswith('#'): continue
        out.append(ln.split('#')[0].rstrip())   # strip inline comment
    return out

def varint(n):
    b=bytearray()
    while True:
        x=n&0x7f; n>>=7
        if n: b.append(x|0x80)
        else: b.append(x); return bytes(b)

def msg_domain(value):
    # Domain{ type=3(FULL)=08 03 ; value=f2 ->12 len v }
    vb=value.encode('utf-8')
    return b'\x08\x03\x12'+varint(len(vb))+vb

def geosite(code, domains):
    body=b'\x0a'+varint(len(code))+code.encode('utf-8')
    for v in domains:
        m=msg_domain(v)
        body+= b'\x12'+varint(len(m))+m
    return body

def top(geosites):
    out=bytearray()
    for g in geosites:
        out+= b'\x0a'+varint(len(g))+g
    return bytes(out)

bl=clean(BL)
wl=clean(WL)
data=top([geosite('BLACKLIST',bl), geosite('WHITELIST',wl)])
open(OUT,'wb').write(data)
print('bl entries:',len(bl),' wl:',len(wl))
print('out bytes :',len(data),'->',OUT)
