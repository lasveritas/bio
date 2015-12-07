e = 0.1

t = 0.1

d = 0.1



S1 = 'AGA' #n i

S2 = 'AGAGA'   #m j



n = len(S1)

m = len(S2)



q1 = dict()

q2 = dict()

p = dict()

for i in xrange(1, n + 1):

    q1[i] = 1.

    p[(i, m + 1)] = 0

    p[(i, 0)] = 0

    for j in xrange(1, m + 1):

        p[(0, j)] = 0

        p[(n + 1, j)] = 0

        p[(i, j)] = 0.9 if S1[i - 1] == S2[j - 1] else 0.1

        q2[j] = 1.

q1[0] = 0

q2[0] = 0

q1[n + 1] = 0

q2[m + 1] = 0

p[(n + 1, m)] = 0

p[(n, m + 1)] = 0



FM = dict()

FX = dict()

FY = dict()



FM[(0, 0)] = 1

FX[(0, 0)] = 0

FY[(0, 0)] = 0



for i in xrange(0, n + 1):

    FM[(i, -1)] = 0

    FX[(i, -1)] = 0

    FY[(i, -1)] = 0



for j in xrange(0, m + 1):

    FM[(-1, j)] = 0

    FX[(-1, j)] = 0

    FY[(-1, j)] = 0



for i in xrange(0, n + 1):

    for j in xrange(0 if i != 0 else 1, m + 1):

        k = (i - 1, j - 1)

        FM[(i, j)] = p[i, j] * ((1 - 2*d - t) * FM[k] + (1 - e - t) * (FX[k] + FY[k]))

        FX[(i, j)] = q1[i] * (d * FM[(i - 1, j)] + e * FX[(i - 1, j)])

        FY[(i, j)] = q2[j] * (d * FM[(i, j - 1)] + e * FY[(i, j - 1)])



E = (n, m)

E = t * (FM[E] + FX[E] + FY[E])

print(E)

BM = dict()

BX = dict()

BY = dict()



BM[(n, m)] = t

BX[(n, m)] = t

BY[(n, m)] = t



for i in xrange(0, n + 1):

    BM[(i, m + 1)] = 0

    BX[(i, m + 1)] = 0

    BY[(i, m + 1)] = 0



for j in xrange(0, m + 1):

    BM[(n + 1, j)] = 0

    BX[(n + 1, j)] = 0

    BY[(n + 1, j)] = 0





for i in xrange(n, -1, -1):

    for j in xrange(m if i != n else m - 1, -1, -1):

        k = (i + 1, j + 1)

        BM[(i, j)] = (1 - 2*d - t) * p[k] * BM[k] + d * (q1[i + 1] * BX[(i + 1, j)] + q2[j + 1] * BY[(i, j + 1)])

        BX[(i, j)] = (1 - e - t) * p[k] * BM[k] + e * q1[i + 1] * BX[(i + 1, j)]

        BY[(i, j)] = (1 - e - t) * p[k] * BM[k] + e * q2[j + 1] * BY[(i, j + 1)]





for i in xrange(1, n + 1):

    print [round(FM[(i, j)] * BM[(i, j)] / E, 3) for j in xrange(1, m + 1)]


