def vis_velkomst():
    print("Velkommen til Mastermind!")
    print("Du skal gætte 4 forskellige tal fra 1 til 4.")

import random

def generer_kode():
    return random.sample(range(1, 5), 4)

def modtag_gaet():
    gaet = input("Indtast 4 tal adskilt af mellemrum: ")
    return list(map(int, gaet.split()))

def tael_rigtige_pladser(kode, gaet):
    count = 0
    for i in range(4):
        if kode[i] == gaet[i]:
            count += 1
    return count

def spil(): 
    while True:
        vis_velkomst()
        kode = generer_kode()
        
        while True:
        gaet = modtag_gaet()

        antal = tael_rigtige_pladser(kode, gaet)

        print("Rigtige pladser:", antal)    

        if antal == 4: 
            print("Tillykke! Du har gættet koden!")
            break   

def spil_igen():
    return input("Vil du spille igen? (j/n): ").lower()




igen = spil_igen()

if igen == "j":
    continue

elif igen == "n":
    print("Tak for spillet!")
    break
