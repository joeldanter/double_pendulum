# Dupla inga kísérletezgetés
Osztályok és függvények gyűjteménye a dupla inga szimulációjához, animálásához, manipulálásához és a vele való kísérletezgetéshez.
Emellett tartalmaz fájlokat amik ezeket használják, esetleg különböző érdekességeket demonstrálnak.

## Installation
1. Clone the repository
```bash
git clone https://github.com/joeldanter/double_pendulum.git
```
2. Enter the directory
```bash
cd double_pendulum
```
4. Create virtual environment
```bash
python -m venv .venv
```
5. Install dependencies
```bash
pip install -r requirements.txt
```

## Használat
Indítsa el a "futtatható" fájlok egyikét
Például:
```bash
python multiple_set_e.py
```

## Files
- `double_pendulum.py`: Osztályokat tartalmaz ami egy dupla inga értékeit és fizikáját kezeli.
- `world.py`: Osztályt tartalmaz, ami egyszerre több dupla ingának a kirajzolását, animálását és időkezelését végzi.
- `plotting.py`: Függvényeket tartalmaz, amik fázisterek kirajzolásához szükségesek.
- `README.md`: Ez a fájl
- `requirements.txt`: Szükséges modulok a projekthez

### Futtathatóak
- `single.py`: Létrehoz egyetlen dupla ingát, leanimáltatja, majd a fázisterét kirajzoltatja.
- `multiple.py`: Létrehoz több dupla ingát minimális eltérésekkel kezdeti állapotukban, leanimáltatja.
- `scatter.py`: Létrehoz több dupla ingát véletlenszerű kezdeti állapotokkal, leanimáltatja.
- `single_set_e.py`: `single.py`, csak beállítja az inga energiáját egy adott értékre.
- `multiple_set_e.py`: `multiple.py`, csak beállítja az ingák energiáit egy adott értékre, fázisterüket kirajzoltatja.
- `scatter_set_e.py`: `scatter.py`, csak beállítja az ingák energiáit egy adott értékre, fázisterüket kirajzoltatja.
- `vector_field.py`: Vektor mezőt rajzol ki.
- `eigenvalues.py`: Csak érdekesség
