# Earth–Sun Gravity Simulation

A small Python/Pygame visualization of an Earth-like body orbiting a fixed Sun under a simplified Newtonian gravity model. The scene includes a scrolling, twinkling star field, a gently pulsing Sun, the orbiting planet, and a fading-length orbit trail. The window title shows the system's total mechanical energy as a live sanity check on the integration.

> This is a visual demonstration using scaled, illustrative parameters — not a precision astronomical model.

## Features

- 2D gravitational orbit computed with a semi-implicit Euler integrator
- Softened inverse-square force to keep the orbit numerically stable
- Live kinetic + potential energy readout in the window title
- Animated star field and orbit trail (capped at 600 points)
- No external assets — pure Pygame drawing primitives

## Requirements

- Python 3.10 or later
- [Pygame](https://www.pygame.org/) 2.5+ (`pip install -r requirements.txt`)

## Installation

```bash
git clone https://github.com/dhergham-fadhil/Solar-System-Gravity-Simulation.git
cd Solar-System-Gravity-Simulation
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python earth_sun_gravity_simulation.py
```

Close the window (or press `Alt+F4` / `Cmd+Q`) to quit. There are no other controls.

## How it works

Each frame the planet's acceleration toward the Sun is computed as

```
a = G * M_sun / (r + softening)^2
```

where `r` is the distance to the Sun. Velocity is updated first, then position (semi-implicit Euler), with a fixed timestep multiplied by a `TIME_SCALE` factor to speed up the visual orbit. Because the units are chosen for appearance rather than realism, `G`, masses, distances and velocities are all illustrative.

## Project structure

```
.
├── earth_sun_gravity_simulation.py   # Simulation and rendering
├── requirements.txt                  # Runtime dependency
└── README.md                         # This file
```

## License

Copyright (c) 2026 dhergham-fadhil. All rights reserved. See [LICENSE](LICENSE).
