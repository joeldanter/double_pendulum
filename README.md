# Dupla inga kísérletezgetés
Osztályok és függvények gyűjteménye a dupla inga szimulációjához, animálásához, manipulálásához és a vele való kísérletezgetéshez.

## Installation
1. Clone the repository
```shell
git clone https://github.com/joeldanter/double_pendulum.git
```
2. Enter the directory
```shell
cd double_pendulum
```
3. Create virtual environment
```shell
python -m venv .venv
```
4. Install dependencies
```shell
pip install -r requirements.txt
```

## Használat
1. Virtuális környezetet aktiválása
```shell
"./.venv/Scripts/activate"
```
2. Futtatás
Fő program
```shell
python main.py
```
Vektormező kirajzolása
```shell
python vector_field.py
```
Érdekesség
```shell
python eigenvalues.py
```

## Files
- `double_pendulum.py`: Osztályokat tartalmaz ami egy dupla inga értékeit és fizikáját kezeli.
- `world.py`: Osztályt tartalmaz, ami egyszerre több dupla ingának a kirajzolását, animálását és időkezelését végzi.
- `plotting.py`: Függvényeket tartalmaz, amik fázisterek kirajzolásához szükségesek.
- `main.py`: Fő program
- `vector_field.py`: Vektor mezőt rajzol ki.
- `eigenvalues.py`: Csak érdekesség
- `README.md`: Ez a fájl
- `requirements.txt`: Szükséges modulok a projekthez
