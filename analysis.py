#!/bin/env python3

import os
import re
import json


results = {}
def shelve(txhash, isCanon, result):
	if txhash not in results :
		results[txhash] = {}
	if isCanon:
		results[txhash]["canon"] = result
	else:
		results[txhash]["alt"] = result


def analyze(txhash, isCanon, fname):
	steps = 0
	gasUsed = 0
	with open("./traces/%s" %  fname,"r") as f:
		lines = f.readlines()
		steps = len(lines)
		if steps > 0:
			res = json.loads(lines[-1])
			gasUsed = res["gasUsed"]
	shelve( txhash, isCanon, ( steps, gasUsed))

xx = sorted(os.listdir("./traces/"))

p = re.compile('block_(?P<blockhash>0x........)-(?P<txindex>[\\d+])-(?P<txhash>0x........).*')
for fname in xx:
	#fname = xx[0]
	m = p.search(fname)
	if m:
		bh = m.group("blockhash")
		tx = m.group("txhash")
		txi = m.group("txindex")
		canon = fname.find("alt") == -1
		analyze(tx, canon, fname)


okCount = 0
brokenCount = 0
tab1 = []
tab2 = []
canGasTot = 0
altGasTot = 0
for k,v in results.iteritems():
	cSteps = int(v["canon"][0])
	aSteps = int(v["alt"][0])
	cGas = int(v["canon"][1], 16)
	aGas = int(v["alt"][1],16)
	if cGas > 0:
		diff = 100 * (aGas-cGas)/ cGas
	else: 
		diff = 0.0
	if cSteps == aSteps:
		ok = "ok"
		okCount +=1
		canGasTot += cGas
		altGasTot += aGas
		tab1.append(" %s | %s | %s | %s | %s | %s | %.2f %%|" % (k,cSteps,aSteps,ok, cGas,aGas, diff)) 
	else:
		ok = "BROKEN"
		brokenCount +=1
		tab2.append(" %s | %s | %s | %s | %s | %s | %.2f %%|" % (k,cSteps,aSteps,ok, cGas,aGas, diff)) 


print("| txhash | steps(canon) | steps(alt) | OK? |  gas(canon) |  gas(alt) | diff | ")
print("| ------ | ------------ | ---------- | --- | -----------| ---------| -----| ")
for elem in tab1:
	print(elem)

print("")
print("")

print("| txhash | steps(canon) | steps(alt) | OK? |  gas(canon) |  gas(alt) | diff | ")
print("| ------ | ------------ | ---------- | --- | -----------| ---------| -----| ")

for elem in tab2:
	print(elem)

print("")
print("")

print ("OK: %d, broken: %d" % (okCount, brokenCount))
print("Canon gas used: %d, alt gas used: %d"% (canGasTot, altGasTot))