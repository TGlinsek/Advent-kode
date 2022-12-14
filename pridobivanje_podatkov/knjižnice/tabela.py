class Vrsta():

    def __init__(self, tabela, indeks):
        self.tabela = tabela
        self.indeks = indeks
        self.jaz = lambda:self.tabela.get_row_copied(self.indeks)  # za metode, ki jih bomo podedovali iz list razreda
    
    def __repr__(self):
        return str(self.tabela.get_row_copied(self.indeks))
    
    def add_elements(self, n=1, default=None):
        # v bistvu samo doda n stolpcev desno od tabele
        self.tabela.safer_set(default, self.tabela.width() - 1 + n, self.indeks, default)
    
    def append(self, el):
        if el is None:
            el = self.tabela.get_default()
        
        self.tabela.safer_set(el, self.tabela.width(), self.indeks)

    def __len__(self):
        return self.tabela.width()
    
    def __iter__(self):
        return self.tabela.iter_row(self.indeks)
        # return iter(self.tabela.get_row_copied(self.indeks))

    def __getitem__(self, ključ):
        # return self.tabela.array[self.indeks][ključ]

        if type(ključ) == slice:
            return self.tabela.get_row_copied(self.indeks)[ključ]

        return self.tabela.get(ključ, self.indeks)

    def __setitem__(self, ključ, vrednost):
        if type(ključ) == slice:
            raise NotImplementedError
        
        # self.tabela.array[self.indeks][ključ] = vrednost
        self.tabela.set(vrednost, ključ, self.indeks)

    def __delitem__(self, ključ):
        if type(ključ) == slice:
            raise NotImplementedError

        # self.tabela.array[self.indeks][ključ] = None
        self.tabela.del_el(ključ, self.indeks)
    
    def extend(self, sez):
        for i in sez:
            self.append(i)
    
    def index(self, el):
        return self.jaz().index(el)
    
    def reverse(self):
        self.tabela.array[self.indeks] = self[::-1]
    

class Stolpec():

    def __init__(self, tabela, indeks):
        self.tabela = tabela
        self.indeks = indeks
        self.jaz = lambda:self.tabela.get_column_copied(self.indeks)
    
    def __repr__(self):
        return str(self.tabela.get_column_copied(self.indeks)) + "^T"

    def add_elements(self, n=1, default=None):
        # samo doda n vrstic pod tabelo
        self.tabela.safer_set(default, self.indeks, self.tabela.height() - 1 + n, default)
    
    def append(self, el):
        if el is None:
            el = self.tabela.get_default()
        
        self.tabela.safer_set(el, self.indeks, self.tabela.height())
    
    def __len__(self):
        return self.tabela.height()

    def __iter__(self):
        return self.tabela.iter_column(self.indeks)

    def __getitem__(self, ključ):
        if type(ključ) == slice:
            return self.tabela.get_column_copied(self.indeks)[ključ]
        
        return self.tabela.get(self.indeks, ključ)

    def __setitem__(self, ključ, vrednost):
        if type(ključ) == slice:
            raise NotImplementedError

        self.tabela.set(vrednost, self.indeks, ključ)

    def __delitem__(self, ključ):
        if type(ključ) == slice:
            raise NotImplementedError

        self.tabela.del_el(self.indeks, ključ)

    def extend(self, sez):
        for i in sez:
            self.append(i)

    def index(self, el):
        return self.jaz().index(el)
    
    def reverse(self):
        self[:] = self[::-1]


class Tabela:
    # vse funkcije so narete tako, da preprečujejo, da bo None kdajkoli element matrike
    # bolje je namesto None imeti kak drug default, odvisno pač od tega, kakšni so ostali elementi v matriki
    # uporabljamo metodo get_default

    def __init__(self, vsebina=[], y=None):
        # y je tudi default element, če vsebina ni pravokotna matrika
        self.array = []
        
        if y is not None and type(vsebina) == int:
            x = vsebina
            self.add_rows(y)
            self.add_columns(x)
            return
        default = y
        
        števila = True
        for i in vsebina:
            self.array.append([])
            for j in i:
                try:
                    self.array[-1].append(int(j))
                except:
                    števila = False
                    break  # hočemo breakati iz obeh zank
            else:
                continue
            break

        if not števila:
            self.array = []
            for i in vsebina:
                self.array.append([])
                for j in i:
                    self.array[-1].append(j)
        
        #if not self.check_if_rectangular(): raise Exception("Vrstice niso enako dolge!")
        self.make_rectangular(default)

    def __repr__(self):
        # return str(self.array)
        l = "[\n"
        for i in range(len(self.array)):
            l += "\t" + str(self.array[i]) + ",\n"
        l += "]"
        return l
    
    def check_if_rectangular(self):
        # preveri, da vse vrstice enako dolge
        return len({len(vrsta) for vrsta in self.array}) <= 1

    def make_rectangular(self, default=None, zahtevana_širina=None):
        if zahtevana_širina is None:
            zahtevana_širina = len(max(self.array, key=len))
        
        if default is None:
            default = self.get_default()
        
        for vrsta in self.array:
            vrsta.extend([default] * (zahtevana_širina - len(vrsta)))

    def get_default(self, vzorec=None):
        # vzorec naj ne bo None: to je le, če ne podamo parametra
        
        slovar = {type(None):None, str:"-", int:0, float:0.0, list:[], dict:{}, set:set(), tuple:tuple(), bool:False}

        if vzorec is None:
            if len(self.array) > 0 and len(self.array[0]) > 0:
                a = self.array[0][0]
                """
                if type(a) in [list, dict, set]:
                    return a.copy()
                return a
                """
                return slovar[type(a)]
            return None
        
        if type(vzorec) == type:
            tip = vzorec
        else:
            tip = type(vzorec)
        
        return slovar[tip]

    def get_empty(self, koord=(0, 0), y=None):
        if y is None:
            x, y = koord
        else:
            x = koord
        
        a = Tabela()
        a.add_rows(y)
        a.add_columns(x)
        return a
        
    def width(self):
        if len(self.array) == 0:
            return 0
        if not self.check_if_rectangular(): raise Exception("Vrstice niso enako dolge!")
        return len(self.array[0])
    
    def height(self):
        return len(self.array)

    def size(self):
        return (self.width(), self.height())
    
    def __len__(self):
        return self.height()
    
    def get(self, koord, y=None):
        if type(koord) == tuple:
            x, y = koord
        else:
            x = koord
        
        if 0 <= y < len(self.array) and 0 <= x < len(self.array[y]):
            return self.array[y][x]
        return None  # default value
    
    def get_row(self, i):
        # ohranja referenco na starševsko tabelo
        return Vrsta(self, i)
    
    def get_row_copied(self, i):
        if 0 <= i < self.height():
            return self.array[i]
        return None
    
    def get_column(self, j):
        # ohranja referenco na starševsko tabelo
        return Stolpec(self, j)

    def get_column_copied(self, j):
        if 0 <= j < self.width():
            return [row[j] for row in self.array]
        return None

    def add_rows(self, n=1, default=None):
        if n < 0:
            return
            # raise Exception(f"Število vrstic mora biti nenegativno število, ne pa {n}!")
        
        if default is None:
            default = self.get_default()
        
        self.array.extend([[default] * self.width() for _ in range(n)])
    
    def add_columns(self, n=1, default=None):
        if n < 0:
            return
            # raise Exception(f"Število stolpcev mora biti nenegativno število, ne pa {n}!")
        
        if default is None:
            default = self.get_default()
        
        # self.array = [vrsta + [default] * n for vrsta in self.array]
        for vrsta in self.array:
            vrsta.extend([default] * n)

    def set(self, vrednost, koord, y=None):
        if type(koord) == tuple:
            x, y = koord
        else:
            x = koord
        
        if 0 <= y < len(self.array) and 0 <= x < len(self.array[y]):
            self.array[y][x] = self.get_default() if vrednost is None else vrednost
        else:
            raise Exception(f"Koordinate {(x, y)} presegajo dimenzije tabele: {(self.width(), self.height())}!")
    
    def __getitem__(self, indeks):
        if type(indeks) == slice:
            raise NotImplementedError

        return self.get_row(indeks)

    def set_row(self, indeks, vrednost):
        if type(vrednost) != list:
            raise Exception(f"{vrednost} bi moral biti seznam, je pa {type(vrednost)}!")
        if len(vrednost) != self.width():
            raise Exception(f"Dolžina seznama mora biti {self.width()}, je pa {len(vrednost)}!")
        
        if 0 <= indeks < self.height():
            if None in vrednost:
                vrednost = list(lambda x: self.get_default() if x is None else x, vrednost)
            self.array[indeks] = vrednost
        else:
            raise Exception(f"Indeks {indeks} presega višino tabele: {self.height()}")
    
    def __setitem__(self, indeks, vrednost):
        if type(indeks) == slice:
            raise NotImplementedError

        self.set_row(indeks, vrednost)
    
    def set_column(self, indeks, vrednost):
        if type(vrednost) != list:
            raise Exception(f"{vrednost} bi moral biti seznam, je pa {type(vrednost)}!")
        if len(vrednost) != self.height():
            raise Exception(f"Dolžina seznama mora biti {self.height()}, je pa {len(vrednost)}!")
        
        if 0 <= indeks < self.width():
            for i, el in enumerate(vrednost):
                self.array[i][indeks] = self.get_default() if el is None else el
        else:
            raise Exception(f"Indeks {indeks} presega širino tabele: {self.width()}")

    def safer_set(self, vrednost, koord, y=None, default=None):
        if type(koord) == tuple:
            x, y = koord
        else:
            if type(koord) != int:
                raise Exception(f"Drugi parameter mora biti ali nabor ali število, ne pa {type(koord)}: {koord}")
            x = koord
        
        if y is None:
            raise Exception("Premalo podanih koordinat!")
        if type(y) != int:
            raise Exception(f"Vrednost je prvi parameter, koordinate pa potem. Tvoj tretji parameter pa je bil {y}")
        

        if y < 0 or x < 0:
            raise Exception(f"Vsaj ena izmed koordinat je negativna: {(x, y)}")
        
        if 0 <= y < len(self.array) and 0 <= x < len(self.array[y]):
            self.array[y][x] = self.get_default() if vrednost is None else vrednost
        else:
            # default = ('-' if type(vrednost) == str else (0 if type(vrednost) == int else None)) if default is None else default
            default = self.get_default(vrednost)
            self.add_rows(y - self.height() + 1, default)
            self.add_columns(x - self.width() + 1, default)
            self.array[y][x] = vrednost

    def del_row(self, indeks):
        if 0 <= indeks < self.height():
            del self.array[indeks]
        else:
            raise Exception(f"Indeks {indeks} izven dometa: {[0, self.height()]}")
        
    def __delitem__(self, indeks):
        if type(indeks) == slice:
            raise NotImplementedError

        self.del_row(indeks)
    
    def del_column(self, indeks):
        if 0 <= indeks < self.width():
            for vrsta in self.array():
                del vrsta[indeks]
        else:
            raise Exception(f"Indeks {indeks} izven dometa: {[0, self.width()]}")
    
    def del_el(self, koord, y=None):
        if type(koord) == tuple:
            x, y = koord
        else:
            x = koord
        
        if 0 <= y < len(self.array) and 0 <= x < len(self.array[y]):
            self.array[y][x] = self.get_default()
        else:
            raise Exception(f"Koordinata {(x, y)} je izven dometa! Dimenzije tabele: {(self.width(), self.height())}")

    def push_row(self, vrsta):
        self.add_rows()
        try:
            self.set_row(self.height() - 1, vrsta)
        except:
            self.del_row(self.height() - 1)

    def append(self, vrsta):
        self.push_row(vrsta)
    
    def push_column(self, stolpec):
        self.add_columns()
        try:
            self.set_column(self.width() - 1, stolpec)
        except:
            self.del_column(self.width() - 1)

    def merge_to_the_right(self, other):
        if self.height() != other.height():
            raise Exception(f"Višini se ne ujemata! self: {self.height()}, other: {other.height()}")
        return Tabela([self[i] + other[i] for i in self.height])
    
    def merge_at_bottom(self, other):
        if self.width() != other.width():
            raise Exception(f"Širini se ne ujemata! self: {self.width()}, other: {other.width()}")
        return Tabela(self.array + other.array)
    
    def transpose(self):
        return Tabela([[row[j] for row in self.array] for j in range(self.width())])
    
    def zrcali_horizontalno(self):
        # čez vertikalno stranico (smer zrcaljenja je pa horizontalna)
        return Tabela([vrsta[::-1] for vrsta in self.array])

    def zrcali_vertikalno(self):
        # čez horizontalno stranico
        return Tabela([vrstica for vrstica in self.array[::-1]])

    def __iter__(self):
        return iter(self.array)

    def iter_row(self, indeks):
        # return iter(self.get_row_copied(indeks))
        return enumerate(iter(self.get_row_copied(indeks)))
    
    def iter_row_reverse(self, indeks):  # TODO: kako narediti iterator, ki vrača elemente vrstice, in pa tudi indeks, le da je indeks takšen, kot je v starševski tabeli (torej, če iteriramo po reverse vrstici, bodo indeksi padali)
        #return iter(self.get_row_copied(indeks)[::-1])
        return reversed(list(enumerate(iter(self.get_row_copied(indeks)[::-1]))))

    def iter_column(self, indeks):
        return enumerate(iter(self.get_column_copied(indeks)))
    
    def iter_column_reverse(self, indeks):
        return reversed(list(enumerate(iter(self.get_column_copied(indeks)[::-1]))))
    
    def iter_from_a_point(self, koord, smer):
        def fun():
            # nonlocal koord
            # nonlocal smer
            x, y = koord
            x_, y_ = smer
            while True:
                el = self.get(x, y)
                if el is None:
                    yield (x, y), el
                    return
                yield (x, y), el
                x += x_
                y += y_
        return fun()
    
    def iter_from_a_point_wrap(self, koord, smer):
        def fun():
            # nonlocal koord
            # nonlocal smer
            x, y = koord
            x_, y_ = smer
            while True:
                el = self.get(x, y)
                if el is None:  # šli smo ven
                    # yield (x, y), el
                    # return
                    
                    if x < 0:
                        x += self.width()
                    elif x >= self.width():
                        x -= self.width()
                    if y < 0:
                        y += self.height()
                    elif y >= self.height():
                        y -= self.height()
                    
                    el = self.get(x, y)
                    if el is None:
                        raise Exception(f"Prevelik korak! Korak je {(x_, y_)}, koord je {(x, y)}, dimenzije tabele {(self.width(), self.height())}")

                yield (x, y), el
                x += x_
                y += y_
        return fun()
    
    def najdi_polje(self, koord, smer, pogoj):
        for (x, y), el in self.iter_from_a_point(koord, smer):
            if pogoj(el, (x, y)):
                return (x, y), el
    
    def najdi_polje_wrap(self, koord, smer, pogoj):
        for (x, y), el in self.iter_from_a_point_wrap(koord, smer):
            if pogoj(el, (x, y)):
                return (x, y), el

    @staticmethod
    def get_line(par1, par2):
        # vrne seznam koordinat
        # simetrična funkcija
        x, y = par1
        x2, y2 = par2
        if x != x2 and y != y2:
            raise Exception(f"Koordinati morata biti v istem stolpcu ali v isti vrstici: {(x, y)}, {(x2, y2)}")
        if x == x2:
            return [(x, u) for u in range(min(y, y2), max(y, y2) + 1)]
        if y == y2:
            return [(w, y) for w in range(min(x, x2), max(x, x2) + 1)]


if __name__ == "__main__":
    a = Tabela([[1, 2], [3, 4], [5, 6]])
    print(a)