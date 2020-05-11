TCC = 20
TCCset = 20
TSC = 30
TSCset = 20

pList = {'tcc': [TCC, TCCset], 'tsc': [TSC, TSCset]}

for p in ['tcc', 'tsc'] :
	for cmd in ['g', 's'] :
		if cmd == 'g' :
			print(pList[p][0])
		elif cmd == 's' :
			val = 10
			print('Before: ', pList[p][1])
			pList[p][1] = val
			print('After: ', pList[p][1])