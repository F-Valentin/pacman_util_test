# Pac-Man Prototype

This project is a small Arcade-based Pac-Man prototype with a menu, a playable maze, and ghost AI.

## Overview

- `src/pac-man.py` launches the game.
- `src/game.py` wires the main menu and level flow.
- `src/level.py` handles the gameplay loop for the active maze.
- `src/entity/player.py` and `src/entity/ghost.py` contain the player and ghost logic.
- `src/maze.py`, `src/cell.py`, and `src/mazegenerator.py` build the maze and pacgum layout.

## Requirements

Install project dependencies with:

```sh
make install
```

## Run the game

```sh
make run
```

You can also point the launcher at a custom config file:

```sh
python3 src/pac-man.py config/config.json
```

## Controls

- Arrow keys or WASD: move the player
- Space: open the pause view

## Development notes

- The configuration file is loaded from `config/config.json`.
- `make lint` runs flake8 and mypy for a quick static check.
