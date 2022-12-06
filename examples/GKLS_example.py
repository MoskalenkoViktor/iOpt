import math
import sys
import unittest

#import subprocess
from subprocess import PIPE, STDOUT, Popen

import numpy as np

from iOpt.problems.GKLS import GKLS
from iOpt.problems.rastrigin import Rastrigin
from iOpt.problems.xsquared import XSquared
from iOpt.solver import Solver
from iOpt.solver_parametrs import SolverParameters

problem = GKLS(2, 1)
#params = SolverParameters(r=3.5, eps=0.01, itersLimit=10000, refineSolution=True)
params = SolverParameters(r=3.5, eps=0.01, refineSolution=True)
solver = Solver(problem, parameters=params)
sol = solver.Solve()
print(sol.numberOfGlobalTrials)
print(sol.numberOfLocalTrials)
print(sol.solvingTime)

print(problem.knownOptimum[0].point.floatVariables)
print(sol.bestTrials[0].point.floatVariables)
print(sol.bestTrials[0].functionValues[0].value)

dim = 4
epsVal = 0.01
rVal = 3.5

#for i in range(100): 
#    with Popen("E:\\ExaMinNew\\globalizer\\_bin\\globalizer_d.exe -lib gkls.dll -N 4 -r 3.5 -eps 0.01 -problem_class Simple -function_number " + str(i+1), stdout=PIPE, stderr=STDOUT, bufsize=1) as p, open('log4D\\log'+ str(i+1)+'.txt', 'ab') as file:
#        for line in p.stdout: # b'\n'-separated lines
#            sys.stdout.buffer.write(line) # pass bytes as is
#            file.write(line)

#for i in range(100): 
#    problem = GKLS(dim, i+1)
#    params = SolverParameters(r=rVal, eps=epsVal, itersLimit=100000, refineSolution=False)
#    solver = Solver(problem, parameters=params)
#    sol = solver.Solve()
#
#    fabsx = 0
#    fm = 0
#    isSolve = 0
#    res = True
#    for j in range(dim): 
#        fabsx = np.abs(problem.knownOptimum[0].point.floatVariables[j] - sol.bestTrials[0].point.floatVariables[j])
#        fm = epsVal * (problem.upperBoundOfFloatVariables[j] - problem.lowerBoundOfFloatVariables[j]);
#        if (fabsx > fm):
#            res = res and False
#
#    
#    if res == True:
#        isSolve = 1
#    print(i+1, sol.numberOfGlobalTrials, isSolve)
#