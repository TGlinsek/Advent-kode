import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..\\..\\..\\pridobivanje_podatkov'))
from poizvedovanje import prenesi, testiraj, pošlji, vhod, vzorec

def rešitev(l, kos=1):
    sez = l.split("\n\n")
    seštej = lambda x: sum(map(int, x.split()))
    if kos == 1:
        return seštej(max(sez, key=seštej))
    return sum(map(seštej, sorted(sez, key=seštej)[-3:]))

pošlji(rešitev)