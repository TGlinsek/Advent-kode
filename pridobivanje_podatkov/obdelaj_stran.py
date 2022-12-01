import re


def vrni_vzorec():    
    return (
        r'.*?'
        r'<pre><code>(?P<vzorec>.+?)</code></pre>'
        r'.*?'
    )


def vrni_rešitvi():
    return (
        r'.*?'
        r'(<code><em>|<em><code>)(?P<res>.+?)(</em></code>|</code></em>)'
        r'.*?'
    )


def vrni_slovar_podatkov_iz_posamezne_strani_igre(niz):
    vzorec = re.compile(
        vrni_vzorec()
        ,
        flags=re.DOTALL
    )
    rešitvi = re.compile(
        vrni_rešitvi()
        ,
        flags=re.DOTALL
    )

    seznam_zadetkov = []
    števec = 0
    for zadetek in vzorec.finditer(niz):
        seznam_zadetkov.append(zadetek.groupdict())
        števec += 1
    """
    if števec != 1:
        pass
        raise Exception("Napačen števec! Števec: " + str(števec))
    """

    seznam_zadetkov2 = []
    for zadetek in rešitvi.finditer(niz):
        seznam_zadetkov2.append(zadetek.groupdict())
    # return seznam_zadetkov[0], *seznam_zadetkov2
    return seznam_zadetkov[0], seznam_zadetkov2[-1]
