#encoding: utf-8

A, B, C, D, E = '12345'

originalMatrix = {(A, B):2.06, 
           (A, C):4.03, (B, C):3.50,
           (A, D):6.32, (B, D):4.12, (C, D):2.25,
           (A, E):2.08, (B, E):5.43,  (C, E):3.65, (D, E):4.81}


   
def group(algorythm):
  distMatrix = originalMatrix.copy()  
  newDistMatrix = {}
  letters = {A, B, C, D, E}
  
  def ordered(i, j):
    if (i, j) in distMatrix:
      return (i, j)
    else:
      return (j, i)
  
  while len(distMatrix.keys()) > 1:
    minDist = min(distMatrix.values())
    for k, v in distMatrix.items():
      if v == minDist:  
        pair, pair_str = k, k[0]+k[1]
        break
        
    letters.discard(k[0])
    letters.discard(k[1])

    for i in letters:
      fk = ordered(k[0], i)
      sk = ordered(k[1], i)
      if algorythm == "wpgma":
        newDistMatrix[(pair_str, i)] = (distMatrix[fk] + distMatrix[sk])/2
      elif algorythm == "upgma":
        newDistMatrix[(pair_str, i)] = (distMatrix[fk]*len(k[0]) + distMatrix[sk]*len(k[1]))/(len(k[0])+len(k[1]))
      del distMatrix[fk]
      del distMatrix[sk]
    del distMatrix[ordered(k[0], k[1])]
  
    letters.add(pair_str)
    distMatrix.update(newDistMatrix)
    newDistMatrix = {}
  return distMatrix  

    
print(group ("wpgma"))
print(group ("upgma"))

  
  
  
  
  