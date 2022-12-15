# https://gist.github.com/MathisHammel/43aa722469a626504de40744dfe0a3da

import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import inspect
from datetime import datetime, timezone, timedelta
import webbrowser

from obdelaj_stran import vrni_slovar_podatkov_iz_posamezne_strani_igre

def vrni_leto():
    return (datetime.now(timezone.utc) - timedelta(hours=5)).year

def vrni_dan():
    # dan na vzhodni obali
    return (datetime.now(timezone.utc) - timedelta(hours=5)).day


load_dotenv()
AOC_COOKIE = os.getenv('AOC_COOKIE')

letos = vrni_leto()
danes = vrni_dan()


def loginaj_in_prenesi(url):
    # print("Stran se prenaša ...")
    with requests.Session() as s:
        try:
            r = s.get(url, headers={'cookie':'session=' + AOC_COOKIE, "User-Agent": "github.com/TGlinsek/Advent-kode by tadej.glinsek@gmail.com"})
        except Exception as e:
            print(f"Napaka pri prenašanju spletne strani! {e}")
            return
        
        status = r.status_code  # to vrne npr 200, 404, itd.

        if status == requests.codes.ok:  # requests.codes.ok so vse veljavne kode
            print("Preneseno!")
            return r.text
        else:
            print("Napaka pri pridobivanju vsebine! Koda: " + str(status))
            return


def navodila(dan=danes, leto=letos):
    print("Navodila se prenašajo!")
    return loginaj_in_prenesi(f'https://adventofcode.com/{leto}/day/{dan}')


def prenesi_input(dan=danes, leto=letos):
    print("Input se prenaša!")
    return loginaj_in_prenesi(f'https://adventofcode.com/{leto}/day/{dan}/input')


def popravi(dan):  # doda 0 na začetek, če je treba
    dan = str(dan)
    return (2 - len(dan)) * "0" + dan


def vrni_pot_za_podatke(dan=danes, leto=letos):
    starš = Path(__file__).parent.parent
    return str(starš) + f"\\podatki\\{leto}\\{popravi(dan)}"


def is_file_full(file, dan=danes, leto=letos):  # is not empty
    mapa = vrni_pot_za_podatke(dan, leto)
    pot = os.path.join(mapa, file)
    if not os.path.exists(pot):
        return False
    with open(pot, "r", encoding='utf-8') as datoteka:  # open vedno išče v mapi z naslovom os.getcwd()
        vsebina = datoteka.read()
    return len(vsebina) != 0


def read_from_file(file, dan=danes, leto=letos):
    # prebere iz fajla
    mapa = vrni_pot_za_podatke(dan, leto)
    pot = os.path.join(mapa, file)
    with open(pot, "r", encoding='utf-8') as datoteka:  # open vedno išče v mapi z naslovom os.getcwd()
        vsebina = datoteka.read()
    return vsebina


def write_to_file(content, file, dan=danes, leto=letos):
    # če ga ni, ustvari fajl
    # vpiše vsebino v fajl

    # mapa = f"...\\{leto}\\{popravi(dan)}"
    mapa = vrni_pot_za_podatke(dan, leto)
    pot = os.path.join(mapa, file)
    with open(pot, 'w', encoding='utf-8') as output:
        output.write(content)


def append_to_file(content, file, dan=danes, leto=letos):
    mapa = vrni_pot_za_podatke(dan, leto)
    pot = os.path.join(mapa, file)
    with open(pot, 'a', encoding='utf-8') as output:
        output.write(content)


def preberi_input(dan=danes, leto=letos, file="input.txt"):
    mapa = vrni_pot_za_podatke(dan, leto)
    pot = os.path.join(mapa, file)
    with open(pot, "r", encoding='utf-8') as f:  # open vedno išče v mapi z naslovom os.getcwd()
        vsebina = []
        while True:
            s = f.readline()
            if s == '':
                break
            vsebina.append(
                "".join(map(str, list(s.rstrip())))
            )
    return vsebina

# https://www.w3schools.com/HTML/html_entities.asp
kode = {
    "nbsp" : " ",
    "lt" : "<",
    "gt" : ">",
    "amp" : "&",
    "quot" : '"',
    "apos" : "'",
    "cent" : "¢",
    "pound" : "£",
    "yen" : "¥",
    "euro" : "€",
    "copy" : "©",
    "reg" : "®"
}

def prečisti(vzorec):
    for koda in kode:
        vzorec = vzorec.replace("&" + koda + ";", kode[koda])
    return vzorec

def prenesi(dan=danes, leto=letos):
    if is_file_full("input.txt", dan, leto) and not is_file_full("output_1.txt", dan, leto):
        print("Nisi še rešil prvega dela!")
        return
    if is_file_full("output_example_2.txt", dan, leto):
        print("Imaš že vse podatke!")
        return
    
    if is_file_full("output_example_1.txt", dan, leto) and not is_file_full("output_example_2.txt", dan, leto) and is_file_full("output_1.txt", dan, leto):
        write_to_file("None", "output_example_2.txt", dan, leto)

    if not is_file_full("input.txt", dan, leto):
        vnos = prenesi_input(dan, leto)
        write_to_file(vnos, "input.txt", dan, leto)


    navod = navodila(dan, leto)

    aux = navod.split("\n")
    aux = aux[:6] + aux[10:-12] + aux[-3:]
    write_to_file("\n".join(aux), "navodila.html", dan, leto)
    mapa = vrni_pot_za_podatke(dan, leto)
    pot = os.path.join(mapa, "navodila.html")

    # https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python:
    webbrowser.open('file://' + os.path.realpath(pot), new=2)  # odpre navodila

    vzorec, *rešitvi = vrni_slovar_podatkov_iz_posamezne_strani_igre(navod)
    vzorec = vzorec['vzorec']
    # print("Vzorec:\n" + vzorec)


    if not is_file_full("input_example.txt", dan, leto):
        vzorec = prečisti(vzorec)
        write_to_file(vzorec, "input_example.txt", dan, leto)
    
    if len(rešitvi) == 1:
        if is_file_full("output_example_1.txt", dan, leto):
            # print(f"Čudno, samo ena rešitev vzorca je bila pridobljena ...: {rešitvi[0]['res']}")  # ne, to ni nič čudnega
            write_to_file(rešitvi[-1]['res'], "output_example_2.txt", dan, leto)
            print("Uspešen drugi del želim!")
        else:
            write_to_file(rešitvi[-1]['res'], "output_example_1.txt", dan, leto)
            print("Uspešen prvi del želim!")
    elif len(rešitvi) == 2:
        if not is_file_full("output_example_1.txt", dan, leto):
            print("Čudno, zakaj pa prva rešitev ni v bazi?")
            write_to_file(rešitvi[0]['res'], "output_example_1.txt", dan, leto)
        
        write_to_file(rešitvi[-1]['res'], "output_example_2.txt", dan, leto)

        print("Rešitvi:", rešitvi)
        print("Uspešen drugi del želim!")
    else:
        if not is_file_full("output_example_1.txt", dan, leto):
            write_to_file(rešitvi[-1]['res'], "output_example_1.txt", dan, leto)
        else:
            write_to_file(rešitvi[-1]['res'], "output_example_2.txt", dan, leto)
        print("Rešitve:", rešitvi)
        print(f"Veliko ({len(rešitvi)}) rešitev je bilo najdenih!")


def is_callable_with(f, *args, **kwargs):
    try:
        return inspect.getcallargs(f, *args, **kwargs)
    except TypeError:
        return False


def testiraj(odgovor, dan=danes, leto=letos, kos=None):
    # TODO naredi tk, da če kličeš z dvema parametroma, bo drugi parameter kos, če pa s tremi, bo drugi parameter dan, tretji pa leto
    # vrne True, če test uspešen

    # testiraj(odgovor, 1)  # kos je 1
    # testiraj(odgovor, 1, 2022)  # dan in leto
    # testiraj(odgovor, 1, 1, 2022) # najprej je kos

    if kos is None:
        kos = is_file_full("output_1.txt", dan, leto) + 1
    print("Del:", kos)


    if str(type(odgovor)) not in ["<class 'function'>", "<class 'builtin_function_or_method'>"]:
        tvoja_rešitev = odgovor
    else:
        # vzorec = read_from_file("input_example.txt", dan, leto)
        vzorec = preberi_input(dan, leto, "input_example.txt")
        if is_callable_with(odgovor, vzorec, kos=kos):
            tvoja_rešitev = odgovor(vzorec, kos=kos)
        else:
            tvoja_rešitev = odgovor(vzorec)
        
    print("Tvoja rešitev:", tvoja_rešitev)
    
    rešitev = read_from_file(f"output_example_{kos}.txt", dan, leto)
    if rešitev == "None":
        print(f"Nimam rešitve za {kos}. del.")
        return
    
    print("Moja rešitev:", rešitev)
    kontrola = str(tvoja_rešitev) == str(rešitev)
    if not kontrola:
        print("Nisva ista.")
    else:
        print("Ista sva.")
    return kontrola


def pošlji(odgovor, dan=danes, leto=letos, kos=None):
    # vrne odgovor na vprašanje "Ali je pravi rezultat nižji od mojega?"
    # če se ne da odgovoriti, vrne None
    
    if kos is None:
        kos = is_file_full("output_1.txt", dan, leto) + 1
    print("Del:", kos)

    if str(type(odgovor)) not in ["<class 'function'>", "<class 'builtin_function_or_method'>"]:
        pass
    else:
        # vnos = read_from_file("input.txt", dan, leto)
        vnos = preberi_input(dan, leto)
        try:
            odgovor = odgovor(vnos, kos)
        except TypeError:  # če smo vnesli preveč parametrov
            odgovor = odgovor(vnos)
    
    print("Tvoj odgovor:", odgovor)
    if is_file_full("output_2.txt", dan, leto):
        moj_odgovor = read_from_file(f"output_{kos}.txt", dan, leto)
        print("Moj odgovor:", moj_odgovor)
        if str(odgovor) != moj_odgovor:
            print("Nisva ista.")
        else:
            print("Ista sva.")
        print("Ta dan si že povsem rešil!")
        return
    
    if is_file_full(f"lower_bound_{kos}.txt", dan, leto):
        lower_bound = int(read_from_file(f"lower_bound_{kos}.txt", dan, leto))
    else:
        lower_bound = float("-inf")

    if is_file_full(f"upper_bound_{kos}.txt", dan, leto):
        upper_bound = int(read_from_file(f"upper_bound_{kos}.txt", dan, leto))
    else:
        upper_bound = float("inf")

    try:
        if int(odgovor) <= lower_bound:
            print(f"TOO LOW. Tvoj odgovor: {odgovor}, lower_bound: {lower_bound}")
            return
        elif int(odgovor) >= upper_bound:
            print(f"TOO HIGH. Tvoj odgovor: {odgovor}, upper_bound: {upper_bound}")
            return
    except:
        pass

    odgovor = str(odgovor)

    if len(odgovor) == 0:
        print("Podal si prazen odgovor!")
        return
    if len(odgovor) == 1:
        print(f"Malo prekratek odgovor: {odgovor}")
        return
    
    if odgovor == "None":
        print("Tvoja funkcija je vrnila None!")
        return

    if is_file_full(f"mistakes_{kos}.txt", dan, leto):
        sez = read_from_file(f"mistakes_{kos}.txt", dan, leto).split("\n")
        if odgovor in sez:
            print(f"Ta odgovor ({odgovor}) si že poizkusil!")
            return

    data = {
      'level': str(kos),
      'answer': odgovor
    }

    print("Pošiljam ...")
    response = requests.post(f'https://adventofcode.com/{leto}/day/{dan}/answer',
                             headers={'cookie':'session=' + AOC_COOKIE}, data=data)

    if 'You gave an answer too recently' in response.text:
        # You will get this if you submitted a wrong answer less than 60s ago.
        print('VERDICT : TOO MANY REQUESTS')
        return  # da ne bomo še bolj serverjev obremenjevali
    elif 'not the right answer' in response.text:
        if 'too low' in response.text:
            print('VERDICT : WRONG (TOO LOW)')
            write_to_file(odgovor, f"lower_bound_{kos}.txt", dan, leto)
        elif 'too high' in response.text:
            print('VERDICT : WRONG (TOO HIGH)')
            write_to_file(odgovor, f"upper_bound_{kos}.txt", dan, leto)
        else:
            print('VERDICT : WRONG (UNKNOWN)')
            append_to_file("\n" + odgovor, f"mistakes_{kos}.txt", dan, leto)
    elif 'seem to be solving the right level.' in response.text:
        # You will get this if you submit on a level you already solved.
        # Usually happens when you forget to switch from `PART = 1` to `PART = 2`
        print('VERDICT : ALREADY SOLVED')
    else:
        print('VERDICT : OK !')
        write_to_file(odgovor, f"output_{kos}.txt", dan, leto)
    prenesi(dan, leto)


def vhod(dan=danes, leto=letos):
    return read_from_file("input.txt", dan, leto)


def vzorec(dan=danes, leto=letos):
    return read_from_file("input_example.txt", dan, leto)


def reši(odgovor, dan=danes, leto=letos, kos=None):
    pravilno = testiraj(odgovor, dan, leto, kos)
    if pravilno:
        pošlji(odgovor, dan, leto, kos)
    else:
        print("Testiranje ni uspelo, ne pošiljam odgovora.")
