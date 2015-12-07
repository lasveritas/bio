#encoding: utf-8
import sys

first_line = sys.argv[1]
second_line = sys.argv[2]

rows = len(first_line) + 1
colomns = len(second_line) + 1

ToEnd = 0.1 #тау
GapStart = 0.1 #сигма
GapExtend = 0.1 #эпсилон

TransToM = 1 - GapExtend - ToEnd
ToM = 1 - 2*GapStart - ToEnd

FM, FX, FY = dict(), dict(), dict()

FM = {(i, -1):0 for i in range(rows)}
FM.update({(-1, j):0 for j in range(colomns)})  
FX = FM.copy()
FY = FM.copy()

FX[(0, 0)] = 0
FY[(0, 0)] = 0
FM[(0, 0)] = 1

qx = [0] +[1 for i in range(rows-1)] + [0]
qy = [0] + [1 for i in range(colomns-1)] + [0]
pxy = {(k1, k2):0.9 if first_line[k1-1] == second_line[k2-1] else 0.1 
       for k1 in range(1, rows) for k2 in range(1, colomns)}
pxy.update({(i, 0):0 for i in range(rows)})
pxy.update({(0, j):0 for j in range(colomns)})
pxy.update({(i, colomns):0 for i in range(rows+1)})
pxy.update({(rows, j):0 for j in range(colomns+1)})

for i in range(rows):
  for j in range(0 if i != 0 else 1, colomns):
    FM[(i, j)] = pxy[(i, j)] * (ToM * FM[(i-1, j-1)] + TransToM * (FX[(i-1, j-1)] + FY[(i-1, j-1)]))
    FX[(i, j)] = qx[i] * (GapStart * FM[(i-1, j)] + GapExtend * FX[(i-1, j)])
    FY[(i, j)] = qy[j] * (GapStart * FM[(i, j-1)] + GapExtend * FY[(i, j-1)])
    
e = (rows-1, colomns-1)   
END = ToEnd * (FM[e] + FX[e] + FY[e])

BM, BX, BY = dict(), dict(), dict()

BM = {(i, colomns):0 for i in range(rows)}
BM.update({(rows, j):0 for j in range(colomns)})  
BX = BM.copy()
BY = BM.copy()

BX[e] = ToEnd
BY[e] = ToEnd
BM[e] = ToEnd

for i in range(rows-1, -1, -1):
  for j in range(colomns-1 if i!=rows-1 else colomns-2, -1, -1): 
    BM[(i, j)] = ToM * pxy[(i+1, j+1)] * BM[(i+1, j+1)] + GapStart * (qx[i+1] * BX[(i+1, j)] + qy[j+1] * BY[(i, j+1)]) 
    BX[(i, j)] = TransToM * pxy[(i+1, j+1)] * BM[(i+1, j+1)] + GapExtend * qx[i+1] * BX[(i+1, j)]
    BY[(i, j)] = TransToM * pxy[(i+1, j+1)] * BM[(i+1, j+1)] + GapExtend * qy[j+1] * BY[(i, j+1)]
    

for i in range(1, rows):
    print [round(FM[(i, j)] * BM[(i, j)] / END, 3) for j in range(1, colomns)]

