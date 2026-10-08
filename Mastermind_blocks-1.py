def vis_velkomst():
    print("Velkommen til Mastermind!")
    print("Indtast 4 forskellige tal fra 1 til 6, fx 1234 og 6543")

import random

"""def generer_kode():
    return random.sample(range(1, 5), 4)"""

def generer_kode():
    return random.sample(range(1, 7), 4)

"""def modtag_gaet():
    gaet = input("Indtast 4 tal adskilt af mellemrum: ")
    return list(map(int, gaet.split()))"""

def modtag_gaet():
    while True:
        tekst = input("Indtast 4 forskellige tal fra 1 til 6: ")

        try:
            gaet = [int(ciffer) for ciffer in tekst]
            print("Dit gæt:", *gaet)
            """gaet = list(map(int, tekst.split()))"""
        except ValueError:
            print("Ugyldigt input. Brug kun tal.")
            continue

        if len(gaet) != 4 or len(set(gaet)) != 4 or any(tal < 1 or tal > 6 for tal in gaet):
            print("Skriv 4 forskellige tal fra 1 til 6.")
            continue

        return gaet


"""def tael_rigtige_pladser(kode, gaet):
    count = 0

    for i in range(4):
        if kode[i] == gaet[i]:
            count += 1
        if kode[i] == gaet[i]:
            count += 1
            print(f"\033[92m{gaet[i]}\033[0m står rigtigt.")
        elif gaet[i] in kode:
            print(f"Tallet \033[93m{gaet[i]}\033[0m er med i koden, men står forkert placeret.")
           
    return count"""

def tael_rigtige_pladser(kode, gaet):
    count = 0

    for i in range(4):
        if kode[i] == gaet[i]:
            count += 1
            print(f"\033[92m{gaet[i]}\033[0m står rigtigt.")
        elif gaet[i] in kode:
            print(f"Tallet \033[93m{gaet[i]}\033[0m er med i koden, men står forkert placeret.")

    return count

"""def tael_rigtige_pladser(kode, gaet):
    count = 0
    for i in range(4):
        if kode[i] == gaet[i]:
            count += 1
    return count"""

def spil(): 
    vis_velkomst()
    print("Du har 5 forsøg til at gætte koden.")
    kode = generer_kode()
    #print(kode)

    count = 0

    while True:
        gaet = modtag_gaet()

        antal = tael_rigtige_pladser(kode, gaet)

        print("Rigtige pladser:", antal)    

        if antal == 4: 
            print("Tillykke! Du har gættet koden!")
            igen = spil_igen()

            if igen == "j":
                kode = generer_kode()
                count = 0
                continue

            elif igen == "n":
                print("Tak for spillet!")
                break
        else:
            count += 1
            if count >= 5:
                igen = spil_igen()
                if igen == "n":
                    print("Tak for spillet!")
                    break
                if igen == "j":
                    kode = generer_kode()
                    count = 0
                    continue

def spil_igen():
    igen = input("Vil du spille igen? (j/n): ").lower()
    return igen
    """if igen == "n":
        print("Tak for spillet!")
        break
    if igen == "j":
        count = 0
        continue"""


if __name__ == "__main__":
    spil()