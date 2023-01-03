import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..\\..\\..\\pridobivanje_podatkov'))
from poizvedovanje import prenesi, testiraj, pošlji, vhod, vzorec, reši

from pathlib import Path
dan, leto = map(int, Path(__file__).parent.parts[-2:][::-1])


prenesi(dan, leto)
def _1(x):
    x = "\n".join(x)
    
    izenačenje = {"A": "X", "B": "Y", "C": "Z"}
    poraz = {"A": "Z", "B": "X", "C": "Y"}

    l = x.split("\n")
    # l = x
    c = 0
    
    for i in l:
        if len(i) == 0:
            continue
        
        a, b = i.split()

        if b == "Y":
            c += 2
        if b == "X":
            c += 1
        if b == "Z":
            c += 3
        
        if izenačenje[a] == b:
            c+=3
        elif poraz[a] == b:
            pass
        else:
            c += 6
    
    return c


def _2(x):
    x = "\n".join(x)

    izenačenje = {"A": "X", "B": "Y", "C": "Z"}
    poraz = {"A": "Z", "B": "X", "C": "Y"}
    zmaga = {"A": "Y", "B": "Z", "C": "X"}
    vrednosti = {"X": 1, "Y": 2, "Z": 3}

    l = x.split("\n")
    # l = x
    c = 0

    for i in l:
        if len(i) == 0:
            continue
        
        a, b = i.split()

        if b == "Y":
            c += vrednosti[izenačenje[a]]
        elif b=="X":
            c += vrednosti[poraz[a]]
        elif b == "Z":
            c += vrednosti[zmaga[a]]

        if b == "Y":
            c += 3
        elif b == "X":
            pass
        else:
            c += 6
    
    return c


# pošlji(_1, dan, leto, 1)
# pošlji(_2, dan, leto, 2)

reši(_1, dan, leto, 1)
reši(_2, dan, leto, 2)
