# https://gist.github.com/MathisHammel/43aa722469a626504de40744dfe0a3da

import requests
import os
from pathlib import Path
from dotenv import load_dotenv

from obdelaj_stran import vrni_slovar_podatkov_iz_posamezne_strani_igre


load_dotenv()
AOC_COOKIE = os.getenv('AOC_COOKIE')

letos = 2022
danes = 1


def loginaj_in_prenesi(url):
    print("Stran se prenaša ...")
    with requests.Session() as s:
        try:
            r = s.get(url, headers={'cookie':'session=' + AOC_COOKIE})
        except Exception as e:
            print(f"Napaka pri prenašanju spletne strani! {e}")
            return
        
        status = r.status_code  # to vrne npr 200, 404, itd.

        if status == requests.codes.ok:  # requests.codes.ok so vse veljavne kode
            print("Stran je prenesena!")
            return r.text
        else:
            print("Napaka pri pridobivanju vsebine! Koda: " + str(status))
            return


def navodila(dan=danes, leto=letos):
    return loginaj_in_prenesi(f'https://adventofcode.com/{leto}/day/{dan}')


def prenesi_input(dan=danes, leto=letos):
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
    with open(pot, "r", encoding='utf-8') as datoteka:  # open vedno išče v imeniku z naslovom os.getcwd()
        vsebina = datoteka.read()
    return len(vsebina) != 0


def read_from_file(file, dan=danes, leto=letos):
    # prebere iz fajla
    mapa = vrni_pot_za_podatke(dan, leto)
    pot = os.path.join(mapa, file)
    with open(pot, "r", encoding='utf-8') as datoteka:  # open vedno išče v imeniku z naslovom os.getcwd()
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


def prenesi(dan=danes, leto=letos):
    if is_file_full("input.txt", dan, leto) and not is_file_full("output_1.txt", dan, leto):
        print("Nisi še rešil prvega dela!")
        return
    if is_file_full("output_example_2.txt", dan, leto):
        print("Imaš že vse podatke!")
        return
    navod = navodila(dan, leto)
    vzorec, *rešitvi = vrni_slovar_podatkov_iz_posamezne_strani_igre(navod)
    vzorec = vzorec['vzorec']
    # print("Vzorec:\n" + vzorec)

    if not is_file_full("input.txt", dan, leto):
        vnos = prenesi_input(dan, leto)
        write_to_file(vnos, "input.txt", dan, leto)
    if not is_file_full("input_example.txt", dan, leto):
        write_to_file(vzorec, "input_example.txt", dan, leto)
    
    if len(rešitvi) == 1:
        if is_file_full("output_example_1.txt", dan, leto):
            print(f"Čudno, samo ena rešitev vzorca je bila pridobljena ...: {rešitvi[0]['res']}")
        write_to_file(rešitvi[0]['res'], "output_example_1.txt", dan, leto)
        # print("Rešitev:", rešitvi)
        print("Uspešen prvi del želim!")
    elif len(rešitvi) == 2:
        if not is_file_full("output_example_1.txt", dan, leto):
            print("Čudno, zakaj pa prva rešitev ni v bazi?")
            write_to_file(rešitvi[0]['res'], "output_example_1.txt", dan, leto)
        
        write_to_file(rešitvi[-1]['res'], "output_example_2.txt", dan, leto)

        print("Rešitvi:", rešitvi)
        print("Uspešen drugi del želim!")
    else:
        print("Rešitve:", rešitvi)
        print(f"Veliko ({len(rešitvi)}) rešitev je bilo najdenih!")


def testiraj(odgovor, dan=danes, leto=letos, kos=None):
    # vrne True, če test uspešen

    if kos is None:
        kos = is_file_full("output_1.txt", dan, leto) + 1
    print("Del:", kos)

    rešitev = read_from_file(f"output_example_{kos}.txt", dan, leto)
    if str(type(odgovor)) not in ["<class 'function'>", "<class 'builtin_function_or_method'>"]:
        tvoja_rešitev = odgovor
    else:
        vzorec = read_from_file("input_example.txt", dan, leto)
        tvoja_rešitev = odgovor(vzorec)
    print("Tvoja rešitev:", tvoja_rešitev)
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
        vnos = read_from_file("input.txt", dan, leto)
        odgovor = odgovor(vnos)
    
    print("Tvoj odgovor:", odgovor)
    if is_file_full("output_2.txt", dan, leto):
        moj_odgovor = read_from_file(f"output_{kos}.txt")
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
