#encoding: utf-8

A, B, C, D, E, F = 'ABCDEF'

originalMatrix = {(A, B):5, 
           (A, C):4, (B, C):7,
           (A, D):7, (B, D):10, (C, D):7,
           (A, E):6, (B, E):9,  (C, E):6, (D, E):5,
           (A, F):8, (B, F):11, (C, F):8, (D, F):9, (E, F):8}


route = []

def group(algorythm):
  global route
  code = {A:0, B:1, C:2, D:3, E:4, F:5}
  
  distMatrix = originalMatrix.copy()  
  newDistMatrix = {}
  letters = {A, B, C, D, E, F}
  
  def ordered(i, j):
    if (i, j) in distMatrix:
      return (i, j)
    else:
      return (j, i)
  
  while len(distMatrix.keys()) >= 1:
    minDist = min(distMatrix.values())
    LR = len(route)
    for k, v in distMatrix.items():
      if v == minDist:  
        pair, pair_str = k, k[0]+k[1]
        code[pair_str] = max(code.values())+1
        route.append([None, None, None, None])
        if len(route) == 1:
          route[0][3] = 2;
        else:
          route[LR][3] = route[LR-1][3] + 1
        route[LR][0] = code[k[0]]
        route[LR][1] = code[k[1]]
        route[LR][2] = minDist * 0.5
        break
        
    letters.discard(k[0])
    letters.discard(k[1])

    for i in letters:
      fk = ordered(k[0], i)
      sk = ordered(k[1], i)
      if algorythm == "wpgma":
        newDistMatrix[(pair_str, i)] = (distMatrix[fk] + distMatrix[sk])*0.5
      elif algorythm == "upgma":
        newDistMatrix[(pair_str, i)] = (distMatrix[fk]*len(k[0]) + distMatrix[sk]*len(k[1]))*1./(len(k[0])+len(k[1]))
      del distMatrix[fk]
      del distMatrix[sk]
    del distMatrix[ordered(k[0], k[1])]
  
    letters.add(pair_str)
    distMatrix.update(newDistMatrix)
    newDistMatrix = {}
    print(route)
  return distMatrix  

    
#------картинко------  
  
from hcluster import dendrogram
import matplotlib.pyplot as plt
from matplotlib import rcParams as par


def draw(alg):
  global route 
  
  par["axes.grid"] = True

  def augmented_dendrogram(*args, **kwargs):
    ddata = dendrogram(*args, **kwargs)
    if not kwargs.get('no_plot', False):
      for i, d in zip(ddata['icoord'], ddata['dcoord']):
        x = 0.5 * sum(i[1:3])
        y = d[1]
        plt.plot(x, y, 'ro')
        plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),textcoords='offset points', va='top', ha='center')
    return ddata

  for i in range(len(route)):
    for v in range(len(route[i])):
      route[i][v] = float(route[i][v])

  letters = [A, B, C, D, E, F]
  augmented_dendrogram (route, labels=letters)
  route = []

  
  if alg == "wpgma":
    plt.savefig('wpgma.pdf')
  elif alg == "upgma":
    plt.savefig('upgma.pdf')
  plt.close()  
    
    
print(group ("wpgma"))
draw("wpgma")

print(group ("upgma"))  
draw("upgma")  
  
