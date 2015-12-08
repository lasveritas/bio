#encoding: utf-8

A, B, C, D, E, F = 'ABCDEF'

originalMatrix = {(A, B):5, 
           (A, C):4, (B, C):7,
           (A, D):7, (B, D):10, (C, D):7,
           (A, E):6, (B, E):9,  (C, E):6, (D, E):5,
           (A, F):8, (B, F):11, (C, F):8, (D, F):9, (E, F):8}


route = {}
check = {}

distMatrix = originalMatrix.copy()  


def group():
  global route
  global distMatrix
  newDistMatrix = {}
  letters = {A, B, C, D, E, F}  
  code = {A:0, B:1, C:2, D:3, E:4, F:5}
  
  def ordered(i, j):
    if (i, j) in distMatrix:
      return (i, j)
    else:
      return (j, i)  

  def distToAll(p):
    lettersRed = letters - {p[0], p[1]}
    N = len(lettersRed)
    distToAll0 = 0
    distToAll1 = 0
    for i in lettersRed:
      fp = ordered(p[0], i) 
      sp = ordered(p[1], i)
      distToAll0 += distMatrix[fp]
      distToAll1 += distMatrix[sp]
    distToAll0 = distToAll0 * 1/ N
    distToAll1 = distToAll1 * 1/ N
    return(distToAll0, distToAll1)    
        
      
  def searchForMin(): 
    mn = distMatrix[distMatrix.keys()[0]]
    pair = distMatrix.keys()[0]
    for i in distMatrix.keys():
      distToAll0, distToAll1 = distToAll(i)
      mn2 = distMatrix[i] - distToAll0 - distToAll1 
      if mn2 < mn:
        mn = mn2
        pair = i
    return (pair, mn)
    
  while len(distMatrix.keys()) >= 3:
    (p, minDist) = searchForMin()
    distToAll0, distToAll1 = distToAll(p)
    pair_str = p[0] + p[1]
     
    route[p[0]] = round(0.5*(distMatrix[p] + distToAll0 - distToAll1),3)
    route[p[1]] = round(0.5*(distMatrix[p] - distToAll0 + distToAll1),3)
    check[pair_str] = (p[0], p[1])

    letters.remove(p[0])  
    letters.remove(p[1])     
    
    for i in letters - {p[0], p[1]}:
      fp = ordered(p[0], i)
      sp = ordered(p[1], i)
     
      newDistMatrix[(pair_str, i)] = 0.5*(distMatrix[fp] + distMatrix[sp] - distMatrix[p])
      
      del distMatrix[fp]
      del distMatrix[sp]
      
    del distMatrix[p]
     
    letters.add(pair_str)
    distMatrix.update(newDistMatrix)
    newDistMatrix = {}

  print(route)  
  return distMatrix

print(group ())
ch = sorted(check.keys(), key=len)[::-1]


f = open('tree.xml', 'w')

def simple_clade(n, l):
  f.write('<clade>\n')
  f.write('<name>{}</name>\n'.format(n))
  f.write('<branch_length>{}</branch_length>\n'.format(l))
  f.write('<confidence type="unknown">{}</confidence>\n'.format(l))
  f.write('</clade>\n')

def clade(l):
  f.write('<clade>\n')
  f.write('<branch_length>{}</branch_length>\n'.format(l))
  f.write('<confidence type="unknown">{}</confidence>\n'.format(l))
  
def wr(i):
  for j in check[i]:
    if len(j) == 1:
      simple_clade(j, route[j])
    else:
      clade(route[j])
      wr(j)
      f.write('</clade>\n') 

f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<phyloxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.phyloxml.org http://www.phyloxml.org/1.10/phyloxml.xsd" xmlns="http://www.phyloxml.org">\n')
f.write('<phylogeny rooted=\"false\">\n')
f.write('<clade>\n')
 
(fp, sp) = distMatrix.keys()[0]
    
f.write('<clade>\n')
    
if len(fp) == 1:
  f.write('<name>{}</name>\n'.format(fp))
  f.write('<branch_length>{}</branch_length>\n'.format(distMatrix.values()[0]))  
  f.write('<confidence type="unknown">{}</confidence>\n'.format(distMatrix.values()[0]))  
else:
  f.write('<branch_length>1</branch_length>\n')
  wr(fp)
  
f.write('</clade>\n')
f.write('<clade>\n')
  
if len(sp) == 1 and len(fp) > 1:
  f.write('<name>{}</name>\n'.format(sp))
  f.write('<branch_length>{}</branch_length>\n'.format(distMatrix.values()[0]))  
  f.write('<confidence type="unknown">{}</confidence>\n'.format(distMatrix.values()[0])) 
else:
  f.write('<branch_length>1</branch_length>\n')  
  wr(sp) 

f.write('</clade>\n')
  
f.write('</clade>\n')
f.write('</phylogeny>\n')
f.write('</phyloxml>\n')
f.close()

from Bio import Phylo
tree = Phylo.read('tree.xml', 'phyloxml')
Phylo.draw(tree)
