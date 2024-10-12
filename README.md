# Projektna-naloga

Avtor: Jure Kraševec

## Uvod

Za analizo podatkov sem izbral spletno stran [Basketball Reference](https://www.basketball-reference.com/), kjer sem poiskal podatke za minulo sezono (2023/24) lige NBA.
Shranil sem html kodo spletne strani, iz katere sem izluščil želene podatke za vsakega igralca, še prej pa sem podatke razdelil na redni del sezone in končnico (playoffs).
S pomočjo knjižnice Pandas sem analiziral podatke igralcev in iskal različne povezave med posameznimi kategorijami podatkov.

## Navodila za uporabo

V datoteki zajem_strani.py je shranjena koda, ki prejme url naslov spletne strani in shrani html kodo v novo datoteko. Datoteka pridobivanje_podatkov.py pa iz dobljene html kode s pomočjo regularnih izrazov izlušči kategorije in podatke za vse igralce. Nato ustvari posebej csv in json datoteki tako za redni del sezone ter končnico. CSV datoteki sta tisti datoteki, ki ju potem v Juptyer Notebook-u s pomočjo knjižnice Pandas najprej uvozimo, kasneje pa z uporabo različnih metod analiziramo košarkarske podatke. 

Uporabljene knjižnice: za pridobivanje podatkov iz spleta potrebujemo knjižnice requests, BeautifulSoup, re, csv in json.