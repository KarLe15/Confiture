import random
import os


def ecrire(file, nb):
    file.write(";" + str(nb))



"""
    Fonction pour generer 100 fois de suites 99 instances aleatoires
"""
def generateur100():
    for tirage in range(1, 101):
        pMax = 100
        for i in range(1,100):

            V = []
            filename = "k" + str(i) + ".csv"
            file = open("Data/CapacitesAleatoires/"+ str(tirage) + "/" + filename, "w")
            file.write("1")
            while len(V) < i-1:
                nbRand = random.randrange(2, pMax)
                if nbRand not in V :
                    V.append(nbRand)
            V.sort()
            for val in V:
                ecrire(file, val)
            file.close()
            print(i)

################################################################################################"
################################################################################################"
################################################################################################"
################################################################################################"


""" 
    Script pour creer les dossiers de tests
"""

def creation_dossier():
    for i in range(1, 101):
        os.mkdir("Res/Ecart/"+ str(i) )

creation_dossier()



# uniforme()
# test()
# generateur100()
