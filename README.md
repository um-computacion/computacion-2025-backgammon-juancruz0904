# Trabajo Final: Backgammon

# Información del Estudiante
- Nombre: Juan Cruz
- Apellido: Sacchi
- Legajo: 63322

# Objetivos
- Poder jugar partidas en el juego Backgammon en esta aplicacion.

# Descripción General
En este trabajo Final, desarrolamos una aplicacion que permite jugar partidas de Backgammon. Para poder desarrollarlo es necesario atender los siguientes aspectos para que el juego funciones:
- Tener Python 3.10.12
- El unittest para efectuar las pruebas unitarias.
- La dispociocion de las carpetas con las aplicaciones y funciones del juego.

# Características
- Juego Básico: Permite a dos jugadores lanzar dados, mover fichas y capturar fichas del oponente, enviándolas a la barra.
- Tirada de Inicio: Determina aleatoriamente qué jugador comienza el juego lanzando un dado cada uno.
- Movimientos de Fichas: Valida los movimientos para asegurar que las fichas se mueven según las reglas del Backgammon, incluida la captura de fichas.
- Dados: Simulación de dos dados. En caso de que los valores sean iguales (dobles), se otorgan 4 movimientos.

# Estructura del Proyecto
El proyecto se divide en varis clases y cada una controla una parte del juego Backgammon.
- main.py: Contiene la lógica principal del juego de línea de comandos, incluyendo la interacción con el usuario y la visualización del tablero.
- game.py: La clase principal BackgammonGame que gestiona el flujo del juego, los turnos, los movimientos y la victoria.
- board.py: Define el tablero de juego (Board) y sus puntos (Point), con la configuración inicial de las fichas.
- dice.py: Simula el lanzamiento de los dados y gestiona los movimientos disponibles.
- player.py: Representa a los jugadores, con su nombre y color de fichas.
- checker.py: Representa una ficha individual.
