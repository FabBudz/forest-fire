# Forest-Fire Model

Symulacja pożaru lasu zaimplementowana jako automat komórkowy w Pythonie z użyciem pygame.

---

## Zasada działania

Siatka składa się z komórek w jednym z trzech stanów: puste pole, drzewo, ogień. Co krok symulacji:

- ogień gaśnie → zostaje puste pole
- drzewo sąsiadujące z ogniem → zaczyna płonąć
- drzewo bez płonącego sąsiada → może się spontanicznie zapalić z prawdopodobieństwem `f`
- puste pole → może wyrosnąć drzewo z prawdopodobieństwem `p`

Stosunek `p/f` decyduje o charakterze symulacji — przy małym `f` pożary są rzadkie ale duże, przy dużym `f` las ledwo zdąży odrosnąć.

---

## Instalacja

### Uwaga nie działa na nowszych wersjach pythona

#Przykładowa instalacja dla python 3.12

py -3.12 -m venv myenv

myenv\Scripts\activate


pip install pygame

python forest_fire.py

## Sterowanie

lewy przyciśk myszki - rozpalenie ognia w miejscu kursora 
+, = - przyspieszenie symulacji
- - 

---

## Parametry

Na górze pliku `forest_fire.py`:

```python
P_TREE    = 0.55    # prawdopodobieństwo odrostu drzewa
P_IGNITE  = 0.0005  # prawdopodobieństwo spontanicznego zapłonu
CELL_SIZE = 8       # rozmiar komórki w pikselach
COLS      = 120     # szerokość siatki
ROWS      = 90      # wysokość siatki
```