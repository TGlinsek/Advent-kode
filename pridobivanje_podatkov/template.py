import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..\\..\\..\\pridobivanje_podatkov'))
from poizvedovanje import prenesi, testiraj, pošlji, vhod, vzorec, reši

from pathlib import Path
dan, leto = map(int, Path(__file__).parent.parts[-2:][::-1])

from knjižnice.tabela import Tabela as tab


prenesi(dan, leto)
def f(l, kos=1):
    l = "\n".join(l)
    
    return

reši(f, dan, leto)
