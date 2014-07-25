#!/usr/bin/python

'''
 The constraints are as follows:
   1. pkgs in wish-list must be installed
   2. all dependencies must be satisfied in complete disk-image
   3. there are no pkgs conflicting with each other in disk-image
 obj. minimize a size of disk-image
 input file includes enum of names of wish-pkgs 
'''

import sys
from itertools import chain
from gurobipy import *

model = Model('package_maker')

if len(sys.argv) < 2:
    print('Usage: package_maker.py filename')
    quit()

f = open("wishes.txt")
wishes = set()
l = f.readline()
while l:
	wishes.add(l.strip())
	l = f.readline()

vars = {}
vars[''] = model.addVar(vtype=GRB.BINARY, name='virtual_package')
f = open("pkgnames_i386.txt")
l = f.readline()
while l:
	vars[l.strip()] = model.addVar(vtype=GRB.BINARY, name=l.strip())
	l = f.readline()

f = open("dest09.txt")
metadata = f.readlines()

model.update()

############################################ make list of constraint

Depends_list = []
Conflicts_list = []
Reccomends_list = [] #ignore
Enhances_list = [] #ignore
Breaks_list = []
Suggests_list = [] #ignore
Replaces_list = [] #ignore
Pre_Depends_list = [] 
orDepends_list = [] # dependency like |depends: package_name
orConflicts_list = []
orReccomends_list = [] #ignore
orEnhances_list = [] #ignore
orBreaks_list = []
orSuggests_list = [] #ignore
orReplaces_list = [] #ignore
orPre_Depends_list = []

def add_cons_list(pkg, obj, cons):
	target = eval(cons + '_list')
	if obj: #emptiness check
		target.append([pkg,obj])

for line in metadata:
	if not line.startswith("  "): 
		pkg = vars[line.strip()]
		
	else:
		l = line.split(": ")
		cons = l[0].strip()
		obj = l[1].strip()
		if ',' in obj:
			obj = obj.split(',')
			obj = map(lambda e: vars[e.strip()], obj)
			cons = 'or' + cons
		else:
			obj = [vars[obj]]
		add_cons_list(pkg, obj, cons)

######################################################

object = LinExpr()
for v in vars.values():
	object.addTerms(1.0,v)
model.setObjective(object,GRB.MINIMIZE) 
#object-function should be more sophisticated but now linear combination

# Fix variables in wish-list
for name in wishes:
    model.addConstr(vars[name] == 1, 'Fix_' + name)

submask = [-1.0,1.0]
addmask = [1.0,1.0]

for j in Depends_list:
	model.addConstr( LinExpr(submask, [j[0],j[1][0]]) >= 0  , 'dependency_' + j[0].varName+ '_to_' + j[1][0].varName)

for j in Pre_Depends_list:
	model.addConstr( LinExpr(submask, [j[0],j[1][0]]) >= 0  , 'pre-dependency_' + j[0].varName+ '_to_' + j[1][0].varName)

for j in Conflicts_list:
	model.addConstr( LinExpr(addmask, [j[0],j[1][0]]) <= 1, 'confliction_' + j[0].varName + '_' + j[1][0].varName)

# for j in Breaks_list:
# 	model.addConstr( LinExpr(submask, [j[0],j[1][0]]) >= 0, 'break_' + j[0].varName + '_' + j[1][0].varName)

for j in orDepends_list:
	linex = LinExpr()
	map(lambda k: linex.addTerms(1.0,k),j[1])
	linex.addTerms(-1.0,j[0])
	model.addConstr( linex >= 0, 'ordependency_for_' + j[0].varName)

model.update()

model.optimize()

model.write('package_maker.lp')

print('')
print('Solved')
print('')

print "Solution: "

for v in vars.values():
	if v.X==1:
		print v.VarName
