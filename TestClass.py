import math
import time
import psutil
import os
import sys
from pathlib import Path


recherche = "RechercheExhaustive"
dynamique = "Algorithme Dynamique"
glouton   = "Algorithme Glouton"


################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"

def RechercheExhaustive(k, V, s):
    x = 0
    if s < 0 :
        return math.inf
    else :
        if s == 0:
            return 0
        else :
            nbCount = s
            for i in range(k):
                x = RechercheExhaustive(k, V, s-V[i])
                if x + 1 <= nbCount :
                    nbCount = x + 1
            return nbCount



################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"


def Glouton(k, V, S):
    A = []
    for i in range(k):
        A.append(0)
    nbBoc = 0
    maxCapa = k - 1
    newS = S
    while newS > 0:
        if newS >= V[maxCapa]:
            newS = newS - V[maxCapa]
            A[maxCapa] = A[maxCapa] + 1
            nbBoc = nbBoc + 1
        else:
            maxCapa = maxCapa - 1
    return (nbBoc, A)

def TestGloutonCompatible(k, V):
    if k >= 3:
        for S in range( (V[2]+2), (V[k-2]+ V[k-1]) ): # pour que V[k-2]+ V[k-1]-1 soit comprise
            for j in range(k):
                if V[j]< S and Glouton(k, V, S)[0] > ( 1 + Glouton(k, V, (S - V[j]))[0] ) :
                    return False
    return True





################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"

NegInf = -1 * math.inf

def BackWord(M, V, k, S, nbBoc):
    A = []
    for i in range(k):
        A.append(0)
    newS = S - 1
    i = k - 1
    nbTemp = 0
    while nbTemp < nbBoc:
        if  i == 0 :
            A[i] = A[i] + newS
            nbTemp = nbTemp + newS
        elif newS == 0:
            A[0] = A[0] + 1
            nbTemp = nbTemp + 1
        elif M[newS][i] == M[newS][i-1]:
            i = i - 1
        elif newS - V[i] < 0 :
            A[i] = A[i] + 1
            nbTemp = nbTemp + 1
        elif (M[newS - V[i]][i] + 1 )== M[newS][i]:
            A[i] = A[i] + 1
            newS = newS - V[i]
            nbTemp = nbTemp + 1
    return A


def calculNbBocaux(M, V, s, i):
    if s == 0 :
        return 0
    if i == 0 and s >= 1 :
        return math.inf
    if s < 0:
        return math.inf
    if M[s-1][i-1] != NegInf:
        return M[s-1][i-1]
    val1 = calculNbBocaux(M, V, s, i-1)
    val2 = calculNbBocaux(M, V, s - V[i-1], i) + 1
    res = min(val1, val2)
    M[s-1][i-1] = res
    return res


def ProgDy(k, V, S):
    M = []
    for i in range(S):
        M.append([])
        for j in range(k):
            M[i].append(NegInf)
    x = calculNbBocaux(M,V, S, k)
    A = BackWord(M, V, k , S , x)
    return (x,A)



################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"

"""
    # Classe utile pour representer une instance de notre probleme
"""

class Probleme :
    def __init__(self, nbBoc, qttConfiture, vectorBoc, typeAlgo):
        self.k = nbBoc
        self.S = qttConfiture
        self.V = vectorBoc
        self.algo = typeAlgo
    def excute(self):
        if self.algo == recherche:
            res = RechercheExhaustive(self.k, self.V, self.S)
            return res
        if self.algo == dynamique:
            res = ProgDy(self.k, self.V, self.S)
            return res
        if self.algo == glouton:
            res = Glouton(self.k, self.V, self.S)
        """ajouter les autres algos"""


"""
    # Classe utile pour effectuer nos tests de temps d'execution et de memoire
"""


class Test :
    def __init__(self, maxK, maxS, typeAlgo):
        self.maxK       = maxK
        self.maxS       = maxS
        self.typeAlgo   = typeAlgo

    def runTests(self):
        for d in [2,3,4]:
            for i in range(3, self.maxK + 1):
                dirPath = "Res/"+self.typeAlgo+"/d"+str(d)+"/"
                fileName = dirPath + "k_"+str(i)+".txt"
                file = open(fileName, "w")
                for j in range(5 , self.maxS):
                    probl = getProblemeFromData(d, i, j, self.typeAlgo)
                    before = time.time()
                    res = probl.excute()
                    after = time.time()
                    duree = after - before
                    print("k = "+ str(i) + "  S = "+ str(j) + "  temps = "+ str(duree) + "   res = "+ str(res))
                    toWrite = str(j) + " " + str(duree) + "\n"
                    file.write(toWrite)
                file.close()
    def runTestMemory(self):
        for d in [2,3,4]:
            for i in range(331, self.maxK + 1):
                dirPath = "Res/memory/" + self.typeAlgo + "/d" + str(d) + "/"
                fileName = dirPath + "k_" + str(i) + ".txt"
                file = open(fileName, "w")
                for j in range(5 , self.maxS):
                    probl = getProblemeFromData(d, i, j, self.typeAlgo)
                    res = probl.excute()
                    process = psutil.Process(os.getpid())
                    memory = process.memory_info().rss
                    toWrite = str(j) + " " + str(memory) + "\n"
                    file.write(toWrite)
                print(i)


################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"

"""
    Fonctions pour lire nos fihciers de tests
"""

def getProblemeFromData(d, k, S, typeAlgo):
    fileName = "Data/d"+str(d)+"/k"+str(k)+".csv"
    return getProblemeFromFile(k, S, fileName, typeAlgo)

def getProblemeFromFile(k, S, fileName, typeAlgo):
    file = open(fileName, "r")
    Vtemp = file.readline().split(";")
    V = list(map(lambda x : int(x), Vtemp))
    return Probleme(k, S, V, typeAlgo)

################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"

"""
    # permet de lire un fichier d'exemple
"""

def LireFichierProbleme(filePath, algo):
    file = open(filePath, "r")
    S = file.readline()
    k = file.readline()
    VTemp = file.readline().split(" ")
    V = list(map(lambda x : int(x) , VTemp))
    return Probleme(k, S, V, algo)



################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"





def runTestExhaustive():
    for i in range(2, 5):
        k = i
        S = 29
        V = list(range(k))
        file = open("Res/RechercheExhaustive/RechercheExhaustive_"+str(i), "w")
        for j in range(S+1):
            before = time.time()
            res = RechercheExhaustive(k, V, j)
            after = time.time()
            duree = after - before
            file.write(str(j)+ " " + str(duree))
        file.close()

# runTestExhaustive()




def runTestDynamique():
    t= Test(333 , 500, dynamique )
    t.runTests()

# runTestDynamique()





def runTestGlouton():
    t= Test(1 , 5000, glouton )
    t.runTests()

# runTestGlouton()





def runQuestion13():
    Compatible = 0
    nonCompatible = 0

    for tirage in range(1, 101):
        tab = []
        for i in range(3,100):
            fileName = "Data/CapacitesAleatoires/"+ str(tirage) +"/k"+str(i)+".csv"
            fRead = open(fileName, "r")
            Vtemp = fRead.readline().split(";")
            V = list(map(lambda x: int(x), Vtemp))
            boolea = TestGloutonCompatible(i, V )
            if boolea :
                Compatible = Compatible + 1
                tab.append(i)
            else :
                nonCompatible = nonCompatible + 1
            print(i)
        print(tab)

    fCompatible = open("Res/GloutonCompatible/compatible.txt", "w")
    fCompatible.write(str(Compatible))
    fCompatible.close()
    fNonCompatible = open("Res/GloutonCompatible/non_compatible.txt", "w")
    fNonCompatible.write(str(nonCompatible))
    fNonCompatible.close()

# runQuestion13()




def runTestQuestion14(f, pMax):
    for i in range(1, 3):
        for j in range(1, 100):
            dirPath = "Data/CapacitesAleatoires/" + str(i) + "/"
            fRead = open( dirPath+"k"+ str(j) + ".csv", "r")
            Vtemp = fRead.readline().split(";")
            V = list(map(lambda x: int(x), Vtemp))
            boolea = TestGloutonCompatible(j, V)
            if not boolea:
                dirPathWrite = "Res/Ecart/" + str(i) + "/"
                fWrite = open(dirPathWrite + str(j) + ".txt", "w")
                minD = pMax
                maxD = f * pMax
                for fn in range(minD, maxD+1):
                    resGlouton = Glouton(j, V, fn)[0]
                    resDyn = ProgDy(j, V, fn)[0]
                    fWrite.write(str(resGlouton) + " " + str(resDyn) + "\n" )
                fWrite.close()
            fRead.close()
            print(str(i) + "       " + str(j))

# runTestQuestion14(5, 100)




def checkEcart():
    ecartTotal = 0
    nb = 0
    pireEcart = 0
    for i in range(1, 3):
        for j in range(1, 100):
            dirPathRead = "Res/Ecart/" + str(i) + "/"
            filePath = dirPathRead + str(j) + ".txt"
            exists = Path(filePath)
            if exists.is_file():
                fRead = open(filePath, "r")
                linesTemp = fRead.readlines()
                lines = list(map(lambda s : s[:-1], linesTemp))
                for l in lines:
                    nums = l.split(" ")
                    ecart = int(nums[0]) - int(nums[1])
                    if ecart > pireEcart :
                        pireEcart = ecart
                    nb = nb + 1
                    ecartTotal = ecartTotal + ecart
    EcartMoyen = ecartTotal / nb
    print(EcartMoyen)
    print(pireEcart)

checkEcart()



def runTestMemory():
    sys.setrecursionlimit(10 ** 9)
    test = Test(333, 1500, dynamique)
    test.runTestMemory()

# runTestMemory()