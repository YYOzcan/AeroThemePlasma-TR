#!/usr/bin/env python3
"""Yeni linux-explorer kaynağında sözlükte olmayan ve daha önce bilinmeyen aday metinleri say."""
import json, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import ceviri1, ceviri2, ceviri3, ceviri4
T = {}
for m in (ceviri1, ceviri2, ceviri3, ceviri4):
    T.update(m.T)
subprocess.run([sys.executable, os.path.join(D, 'aday.py'), sys.argv[1]], stdout=subprocess.DEVNULL, check=True)
aday = json.load(open(os.path.join(D, '..', 'aday.json')))
bilinen = set(json.load(open(os.path.join(D, '..', 'bilinen-atlananlar.json'))))
yeni = [x for x in aday if x['metin'] not in T and x['metin'] not in bilinen]
json.dump(yeni, open(os.path.join(D, '..', 'yeni-cevrilmemis.json'), 'w'), ensure_ascii=False, indent=1)
print(len(yeni))
