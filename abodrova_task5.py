#encoding: utf-8
import sys

first_line = []
second_line = []
matrix = [] #матрица с весами
route = {} #словарь типа: номер клетки-номер исходной клетки
gap = 0.49
change = 1

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
    
#заполняем первый ряд и первый столбец    
for i in range(1, rows):
  matrix[i][0] = matrix[i-1][0] - gap
  route[(i, 0)] = (i-1, 0)
      
for j in range(1, colomns):
  matrix[0][j] = matrix[0][j-1] - gap
  route[(0, j)] = (0, j-1) 
    
#выбираем максимальное значение     
def environment(i, j):
  if first_line[i] == second_line[j]:
    diag = matrix[i-1][j-1] + 1
  else:
    diag = matrix[i-1][j-1] - change
  up = matrix[i-1][j] - gap
  left = matrix[i][j-1] - gap
  
  mx = max(diag, up, left)
  
  if mx == diag:
    return ((i-1, j-1), diag)
  if mx == up:
    return ((i-1, j), up)
  if mx == left:
    return ((i, j-1), left)
  
    
for el in range(1, rows):
  for i in range(el, rows):
    matrix[i][el] = environment(i, el)[1]
    route[(i, el)] = environment(i, el)[0]
  for j in range(el+1, colomns):
    matrix[el][j] = environment(el, j)[1]
    route[(el, j)] = environment(el, j)[0]
   
   
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