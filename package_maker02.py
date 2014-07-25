#!/usr/bin/python

'''
 The constraints are as follows:
   1. pkgs in wish-list must be installed
   2. all dependencies must be satisfied in complete disk-image
   3. there are no pkgs conflicting with each other in disk-image

 obj. minimize a size of disk-image
 input file includes enum of names of wish-pkgs 
'''

DEPEND = 1
CONFLICT = 2

import sys
import re
from gurobipy import *

if len(sys.argv) < 2:
    print('Usage: package_maker.py filename')
    quit()

f = open("wishes.txt")
wishes = []
l = f.readline()
while l:
	wishes.append(l.strip())
	l = f.readline()

f = open("pkgnames_test.txt")
pkgnames = []
l = f.readline()
while l:
	pkgnames.append(l.strip())
	l = f.readline()

n = len(pkgnames) # num of pkgs

#white space in metadata will be used for get metadata
f = open("easy_depends2.txt")
metadata = f.readlines()


model = Model('package_maker')

############################################ make list of constraint

def add_cons_list(pkg, cons, obj_seq):
	target = eval(cons + '_list')
	for obj_seq in obj:
		target.append([pkg,obj])

Depends_list = []
Conflicts_list = []
Reccomend_list = []
Enhances_list = []
Breaks_list = []
Suggests_list = []
Replaces_list = []
PreDepends_list = []
andDepends_list = [] 

print metadata

for line in metadata:
	obj = []
	if virtual_flag:
		pkg = virtual_pkg
		if line.startswith("    "):
			obj.append(line)

	if not line.startswith(" "): 
		pkg = line.strip()
	elif line.startswith(" |"): # or case
		l = line.split(": ")
		cons = l[0].strip()
		obj.append( l[1].strip() )
		if obj.startswith("<"): # it means virtual-package
			virtual_flag = True
			virtual_pkg = 
	else:
		l = line.split(": ")
		cons = l[0].strip()
		obj.append( l[1].strip() )
		if obj.startswith("<"): # it means virtual-package
			virtual_flag = True
			virtual_pkg = obj.remove(['<','>')
		add_cons_list(pkg, cons, obj)

######################################################
# print Depends_list

vars = {}
for i in range(n):
    vars[i] = model.addVar(vtype=GRB.BINARY, name='v'+str(i))

model.update()

model.setObjective(quicksum(vars[i] for i in range(n)),GRB.MINIMIZE) #object-function should be more sophisticated but now linear combination

# Fix variables in wish-list

for name in wishes:
    j = pkgnames.index(name)
    model.addConstr(vars[j] == 1, 'Fix_' + pkgnames[j])

# dependent constraint

for j in Depends_list:
	left_i = pkgnames.index(j[0])
	right_i = pkgnames.index(j[1])
	# express implication in linear polynomial format
	model.addConstr( vars[right_i]-vars[left_i] >= 0  , 'dependency_' + str(left_i)+ '_to_' + str(right_i))

# conflict constraint

for j in Conflicts_list:
	left_i = pkgnames.index(j[0])
	right_i = pkgnames.index(j[1])
	#express !(v1 and v2) in linear polynomial format
	model.addConstr(vars[left_i]+vars[right_i] <= 1, 'confliction_' + str(left_i) + '_' + str(right_i))



model.optimize()

model.write('package_maker.lp')

print('')
print('Solved')
print('')

# result

print "Solution: "

for i in range(n):
	if vars[i].x==1:
		print vars[i].varname
