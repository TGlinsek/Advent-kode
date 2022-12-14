class Tabela:

    def __init__(self, vsebina=[], y=None):
        self.array = []
        
        if y is not None:
            x = vsebina
            self.add_rows(y)
            self.add_columns(x)
            return
        
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
        
        if not self.check_if_rectangular(): raise Exception("Vrstice niso enako dolge!")
        
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
    
    def get(self, koord, y=None):
        if type(koord) == tuple:
            x, y = koord
        else:
            x = koord
        
        if 0 <= y < len(self.array) and 0 <= x < len(self.array[y]):
            return self.array[y][x]
        return None  # default value
    
    def get_row(self, i):
        if 0 <= i < self.height():
            return self.array[i]
        return None
    
    def get_column(self, j):
        if 0 <= j < self.width():
            return [row[j] for row in self.array]
        return None

    def add_rows(self, n=1, default=None):
        if n < 0:
            raise Exception(f"Število vrstic mora biti nenegativno število, ne pa {n}!")
        self.array.extend([[default] * self.width() for _ in range(n)])
    
    def add_columns(self, n=1, default=None):
        if n < 0:
            raise Exception(f"Število stolpcev mora biti nenegativno število, ne pa {n}!")
        # self.array = [vrsta + [default] * n for vrsta in self.array]
        for vrsta in self.array:
            vrsta.extend([default] * n)

    def set(self, vrednost, koord, y=None):
        if type(koord) == tuple:
            x, y = koord
        else:
            x = koord
        
        if 0 <= y < len(self.array) and 0 <= x < len(self.array[y]):
            self.array[y][x] = vrednost
        else:
            raise Exception(f"Koordinate {(x, y)} presegajo dimenzije tabele: {(self.width(), self.height())}!")
    
    def __getitem__(self, indeks):
        return self.get_row(indeks)

    def set_row(self, indeks, vrednost):
        if type(vrednost) != list:
            raise Exception(f"{vrednost} bi moral biti seznam, je pa {type(vrednost)}!")
        if len(vrednost) != self.width():
            raise Exception(f"Dolžina seznama mora biti {self.width()}, je pa {len(vrednost)}!")
        
        if 0 <= indeks < self.height():
            self.array[indeks] = vrednost
        else:
            raise Exception(f"Indeks {indeks} presega višino tabele: {self.height()}")
    
    def __setitem__(self, indeks, vrednost):
        self.set_row(indeks, vrednost)
    
    def set_column(self, indeks, vrednost):
        if type(vrednost) != list:
            raise Exception(f"{vrednost} bi moral biti seznam, je pa {type(vrednost)}!")
        if len(vrednost) != self.height():
            raise Exception(f"Dolžina seznama mora biti {self.height()}, je pa {len(vrednost)}!")
        
        if 0 <= indeks < self.width():
            for i, el in enumerate(vrednost):
                self.array[i][indeks] = el
        else:
            raise Exception(f"Indeks {indeks} presega širino tabele: {self.width()}")

    def safer_set(self, vrednost, koord, y=None):
        if type(koord) == tuple:
            x, y = koord
        else:
            x = koord
        
        if y < 0 or x < 0:
            raise Exception(f"Vsaj ena izmed koordinat je negativna: {(x, y)}")
        
        if 0 <= y < len(self.array) and 0 <= x < len(self.array[y]):
            self.array[y][x] = vrednost
        else:
            self.add_rows(y - self.height() + 1)
            self.add_columns(x - self.width() + 1)
            self.array[y][x] = vrednost

    def del_row(self, indeks):
        if 0 <= indeks < self.height():
            del self.array[indeks]
        else:
            raise Exception(f"Indeks {indeks} izven dometa: {[0, self.height()]}")
        
    def __delitem__(self, indeks):
        self.del_row(indeks)
    
    def del_column(self, indeks):
        if 0 <= indeks < self.width():
            for vrsta in self.array():
                del vrsta[indeks]
        else:
            raise Exception(f"Indeks {indeks} izven dometa: {[0, self.width()]}")
    
    def push_row(self, vrsta):
        self.add_rows()
        try:
            self.set_row(self.height() - 1, vrsta)
        except:
            self.del_row(self.height() - 1)
    
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
        return iter(self.get_row(indeks))
    
    def iter_row_reverse(self, indeks):  # TODO: kako narediti iterator, ki vrača elemente vrstice, in pa tudi indeks, le da je indeks takšen, kot je v starševski tabeli (torej, če iteriramo po reverse vrstici, bodo indeksi padali)
        return iter(self.get_row(indeks)[::-1])
    
    def iter_column(self, indeks):
        return iter(self.get_column(indeks))
    
    def iter_column_reverse(self, indeks):
        return iter(self.get_column(indeks)[::-1])
    
