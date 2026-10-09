# Traffic Escape

Cross 8 lanes of oncoming traffic to reach the other side (Frogger-style).

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| A/D or Left/Right | Change lane |
| W / UP | Move forward |
| S / DOWN | Move back |
| R | Restart |

## Tasks to Complete

### Task 1: Lives System
> Give the player 3 lives. Getting hit loses one; game over at 0.



### Task 2: Moving Log/Raft Lane
> Add a safe lane where the player must hop on a moving log to cross.



### Task 3: High Score Table
> Track and display the top 5 scores across sessions (save to JSON).


### Task 4: Day/Night Cycle
> Every 30 seconds switch between day and night. At night, cars have headlights visible further ahead.


## Folder Structure

```
traffic-escape/
├── main.py
├── requirements.txt
├── Chat_History.pdf
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── high_scores.py
│   ├── player.py
│   ├── raft.py
│   └── traffic.py
├── tests/
│   └── test_game.py
├── videos/
│   ├── before.mp4
│   └── after.mp4
└── README.md
```

## Submission Checklist

- [x] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior (`videos/before.mp4`)
- [x] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working (`videos/after.mp4`)
- [x] Chat history exported as a PDF (`Chat_History.pdf`)



## Completed Lab 4 features

- Three lives, 1.5-second flashing protection after respawn, and game over after the third hit.
- Moving rafts in the river strip: keep your player's center over a raft; water or drifting off the edge costs a life. Traffic cannot hit you in this strip.
- Top five scores saved beside `main.py` in `high_scores.json`, including on restart and quit. A finish awards 100 bonus points. Scores use the original survival-time scoring.
- Day/night switches every 30 seconds of active gameplay. Cars project headlights 170 pixels ahead at night.
- Fixed movement below the screen, unsafe starting sidewalk collisions, and truncated fractional car speeds.

## Verification

```bash
python -m unittest discover -s tests -v
```

Seven tests cover boundary movement, three collisions and restart, respawn protection, raft/water behavior, lighting boundaries, fractional traffic speeds, winning, JSON persistence, and invalid score data.

## Submission evidence

- `videos/before.mp4`: A 10-second continuous gameplay recording of the original starter game, demonstrating the off-screen bottom movement bug and instant game over on car collision (no lives system).
- `videos/after.mp4`: A 10-second continuous gameplay recording of the updated game, demonstrating all 4 completed tasks: boundary safety, the 3-lives system with flashing respawn invulnerability, riding the river raft to safely cross, nighttime transition with directional headlights, and victory.
- `Chat_History.pdf`: An exported 4-iteration Vibe Coding prompt history transcript documenting the iterative prompting process used by Dhruv U to fix bugs, implement each task modularly, write tests, and verify deliverables.


Each numbered task has its own commit. `traffic-escape.bundle` preserves the original and changed commits for import into a personal repository. `changes.patch` preserves the same commit sequence as mail patches.

The original assignment repository has not been modified and no upstream pull request was opened.
