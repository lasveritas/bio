#encoding: utf-8
import sys

first_line = []
second_line = []
matrix = [] #матрица с весами
route = {} #словарь типа: номер клетки-номер исходной клетки
gap = 0.3
change = 2
match = 1

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
    
 
#выбираем максимальное значение     
def environment(i, j):
  if first_line[i] == second_line[j]:
    diag = matrix[i-1][j-1] + match
  else:
    diag = matrix[i-1][j-1] - change
  up = matrix[i-1][j] - gap
  left = matrix[i][j-1] - gap
  
  mx = max(diag, up, left, 0)
 
  if mx == 0:
    return ((-1, -1), 0)  
  if mx == diag:
    return ((i-1, j-1), diag)
  if mx == up:
    return ((i-1, j), up)
  if mx == left:
    return ((i, j-1), left)

  
end = (0, 0)
end_weight = 0    
  
for el in range(1, rows):
  for i in range(el, rows):
    matrix[i][el] = environment(i, el)[1]
    if matrix[i][el] > end_weight:
      end_weight = matrix[i][el]
      end = (i, el)
    route[(i, el)] = environment(i, el)[0]  
  for j in range(el+1, colomns):
    matrix[el][j] = environment(el, j)[1]
    if matrix[el][j] > end_weight:
      end_weight = matrix[el][j]
      end = (el, j)    
    route[(el, j)] = environment(el, j)[0]
   
al = [end] 
n = route[end]
al.append(n)

while matrix[n[0]][n[1]] !=0:
  n = route[n]
  al.append(n)
  
    
f_line = ""
s_line = ""


#выравнивание строк
if(n[0]==n[1]):
  for i in range(1, n[0]+1):
    f_line += first_line[i].lower()
    s_line += second_line[i].lower()
  
if (n[0] > n[1]):
  diff = n[0]-n[1]
  for i in range(1, n[0]+1):
    f_line += first_line[i].lower()
  s_line += " " * diff
  for i in range(1, n[1]+1):
    s_line += second_line[i].lower()

if (n[1]>n[0]):  
  diff = n[1]-n[0]
  for i in range(1, n[1]+1):
    s_line += second_line[i].lower()
  f_line += " " * diff
  for i in range(1, n[0]+1):
    f_line += first_line[i].lower()  

 
f_ln = ""
s_ln = ""

for i in range(1, len(al)):
  if al[i][0] == al[i-1][0]:
    f_ln += "-"
    s_ln += second_line[al[i-1][1]].upper()
  elif al[i][1] == al[i-1][1]:  
    f_ln += first_line[al[i-1][0]].upper()
    s_ln += "-"
  else:
    f_ln += first_line[al[i-1][0]].upper()
    s_ln += second_line[al[i-1][1]].upper()
    
f_line += f_ln[::-1]
s_line += s_ln[::-1]

for i in range(end[0]+1, rows):
  f_line += first_line[i]
for i in range(end[1]+1, colomns):
  s_line += second_line[i] 
    
   
print(f_line)
print(s_line)

print ('\n'+"the best local alignmant: ")
print(f_ln[::-1])
print(s_ln[::-1])
print ('\n'+"alignment weight: "+ str(matrix[end[0]][end[1]]))
