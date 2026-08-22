# Tower Defence
Cílem práce bylo implementovat 2D počítačovou
hru (Tower Defence) v Pythonu pomocí knihovny
pygame. Hráč brání cíl před nepřáteli pomocí obranných věží, 
které automaticky útočí na procházející nepřátelské jednotky. 
Hra umožňuje postupné vylepšování věží za peníze, které
hráč získá zabitím nepřátel. Nepřátelé chodí po de-
finované trase a věže jdou postavit jen na předem
určená místa. Hráč prohraje ve chvíli, když se do cíle
dostane určitý počet nepřátel a vyhrává ve chvíli,
když je počet životů > 0 a už nezbývají žádné další
vlny - resp. nejsou tam už žádní nepřátelé.

Více info o hře a ukázka je v reportu "hableden.pdf".

## Spuštění hry:
```
python src/main.py
```

## Spuštění testů:
```
python -m pytest -v
```

