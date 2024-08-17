# Dupla inga kísérletezgetés
Osztályok és függvények gyűjteménye a dupla inga szimulációjához, animálásához, manipulálásához és a vele való kísérletezgetéshez.

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
Fő program futtatásához:
```bash
python main.py
```
Vektormező kirajzolásához:
```bash
python vector_field.py
```
Érdekesség:
```bash
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
