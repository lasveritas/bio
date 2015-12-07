#encoding: utf-8
import sys

first_line = []
second_line = []

A = [] #матрица с вероятностями
B = []
C = []

gap_start = 2
gap = -1
mismatch = -1
match = 1

route = {} 

#для определённости первая строка будет меньшей из данных
if len(sys.argv[1]) >= len(sys.argv[2]):
  first_line[0:] = "-" + sys.argv[2]
  second_line[0:] = "-" + sys.argv[1]

else:
  first_line[0:] = "-" + sys.argv[1]
  second_line[0:] = "-" + sys.argv[2]  

rows = len(first_line)
colomns = len(second_line)


for i in range(rows):
  A.append([0] * colomns)
  B.append([0] * colomns)
  C.append([0] * colomns) 

A[0][0] = 0
B[0][0] = float("inf")*(-1) 
C[0][0] = float("inf")*(-1)

#route[('A', (0, 0))] = 'A'

#заполняем первый ряд и первый столбец    
for i in range(1, rows):
  A[i][0] = gap_start + (i)*(gap)
  B[i][0] = gap_start + (i)*(gap)
  C[i][0] = float("inf")*(-1) 
  route[('B', (i, 0))] = ('B', (i-1, 0))  
  route[('A', (i, 0))] = ('B', (i-1, 0)) 
  
for j in range(1, colomns):
  A[0][j] = gap_start + (j)*(gap)
  B[0][j] = float("inf")*(-1)
  C[0][j] = gap_start + (j)*(gap)   
  route[('C', (0, j))] = ('C', (0, j-1))
  route[('A', (0, j))] = ('C', (0, j-1))

  
def mx(a):
  num = a.index(max(a))
  if num == 0:
    mt = 'A'
  elif num == 1:
    mt = 'B'
  else:
    mt = 'C'
  return [mt, max(a)]
  
  
#выбираем максимальное значение     
def environment(i, j):
  btry = mx([A[i-1][j]+gap_start+gap, B[i-1][j]+gap, float('inf')*(-1)])
  B[i][j] = btry[1]
  route[('B', (i, j))] = (btry[0], (i-1, j)) 
  
  ctry = mx([A[i][j-1]+gap_start+gap, float('inf')*(-1), C[i][j-1]+gap])
  C[i][j] = ctry[1]
  route[('C', (i, j))] = (ctry[0], (i, j-1))
  
  eq = mismatch
  if first_line[i] == second_line[j]:
    eq = match
  
  atry = mx([A[i-1][j-1]+eq, B[i][j], C[i][j]])
  A[i][j] = atry[1]  
  if atry[0] == 'A':
    route[('A', (i, j))] = ('A', (i-1, j-1))
  else:
    route[('A', (i, j))] = (atry[0], (i, j))

  
for el in range(1, rows):
  for i in range(el, rows):
    env = environment(i, el)

  for j in range(el+1, colomns):
    env = environment(el, j)

rr = ''
n = ('A', (rows-1, colomns-1))
rr += n[0]

while n[1] != (0, 0):
  n = route[n]
  rr += n[0]  
    
rr = rr.replace('AC', 'C')
rr = rr.replace('AB', 'B')

f_line = ''
s_line = ''



fcount = rows - 1
scount = colomns - 1
for i in range(0, len(rr)):
  
  if rr[i] == 'B':
    f_line += first_line[fcount]
    s_line += '-'
    fcount -= 1
  
  elif rr[i] == 'C':
    f_line += '-'
    s_line += second_line[scount]
    scount -= 1
  
  elif rr[i] == 'A': 
    f_line += first_line[fcount]
    s_line += second_line[scount]
    fcount -= 1
    scount -= 1
    
  
if f_line[::-1][0] == '-' and s_line[::-1][0] =='-':
  print(f_line[::-1][1:])
  print(s_line[::-1][1:])
else:
  print(f_line[::-1])
  print(s_line[::-1])

print ('\n'+"alignment weight: "+ str(A[rows-1][colomns-1]))
