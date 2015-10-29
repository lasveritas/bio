#encoding: utf-8
import sys

first_line = []
second_line = []
matrix = [] #матрица с весами
route = {} #словарь типа: номер клетки-номер исходной клетки
gap_start = 15
gap = 7
change = 20
match = 10

#для определённости первая строка будет меньшей из данных
if len(sys.argv[1]) >= len(sys.argv[2]):
  first_line[0:] = "-" + sys.argv[2]
  second_line[0:] = "-" + sys.argv[1]

else:
  first_line[0:] = "-" + sys.argv[1]
  second_line[0:] = "-" + sys.argv[2]  

rows = len(first_line)
colomns = len(second_line)

#инициализация матрицы нулями
for i in range(rows):
    matrix.append([0] * colomns)

direction = {}
direction[(0, 0)] = "diag"
    
#заполняем первый ряд и первый столбец    
for i in range(1, rows):
  matrix[i][0] = matrix[i-1][0] - gap
  route[(i, 0)] = (i-1, 0)
  direction[(i, 0)] = "up"
  
for j in range(1, colomns):
  matrix[0][j] = matrix[0][j-1] - gap
  route[(0, j)] = (0, j-1)
  direction[(0, j)] = "left"

  
  
#выбираем максимальное значение     
def environment(i, j):
  
  pdu = direction[(i-1, j)]
  pdd = direction[(i-1, j-1)]
  pdl = direction[(i, j-1)]
  if pdu == "up":
    up = matrix[i-1][j] - gap     
  else: 
    up = matrix[i-1][j] - gap_start - gap
  if pdl == "left":
    left = matrix[i][j-1] - gap 
  else:
    left = matrix[i][j-1] - gap_start - gap 
   
  if first_line[i] == second_line[j]:
    diag = matrix[i-1][j-1] + match
  else:
    diag = matrix[i-1][j-1] - change    
  
  mx = max(diag, up, left)
  
  if mx == diag:
    return ((i-1, j-1), diag, "diag")
  if mx == up:
    return ((i-1, j), up, "up")
  if mx == left:
    return ((i, j-1), left, "left")  
   
for el in range(1, rows):
  for i in range(el, rows):
    env = environment(i, el)
    matrix[i][el] = env[1]
    route[(i, el)] = env[0]
    direction[(i, el)] = env[2]
  for j in range(el+1, colomns):
    env = environment(el, j)
    matrix[el][j] = env[1]
    route[(el, j)] = env[0]
    direction[(el, j)] = env[2]
   
   
al = [(rows-1, colomns-1)] 
n = route[(rows-1, colomns-1)]
al.append(n)

while n != (0, 0):
  n = route[n]
  al.append(n)

f_line = ""
s_line = ""
  
#выравнивание строк  
for i in range(1, len(al)):
  if al[i][0] == al[i-1][0]:
    f_line += "-"
    s_line += second_line[al[i-1][1]]
  elif al[i][1] == al[i-1][1]:  
    f_line += first_line[al[i-1][0]]
    s_line += "-"
  else:
    f_line += first_line[al[i-1][0]]
    s_line += second_line[al[i-1][1]]
    
print(f_line[::-1])
print(s_line[::-1])

print ('\n'+"alignment weight: "+ str(matrix[rows-1][colomns-1]))