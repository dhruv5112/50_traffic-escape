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
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── player.py
│   └── traffic.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history


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

`videos/before.mp4` is a 10-second recording of the original game, with scripted Down input showing the off-screen movement bug.

`videos/after.mp4` is a 10-second montage rendered by the real updated Pygame game with scripted keyboard input: 2 seconds showing the repaired boundary, 5 seconds showing a raft crossing and finish, and 3 seconds spanning gameplay seconds 29-32 to show the normal lighting transition. No gameplay state was teleported or fabricated for the recordings. The omitted wait and montage are labeled. Run the game yourself for an interactive demonstration.

`Chat_History.pdf` contains the user-facing conversation available at packaging time. For the complete platform chat, including the final response, use ChatGPT's Share control and submit that URL if your instructor requires a page link. This environment cannot obtain or publish a ChatGPT share URL.

Each numbered task has its own commit. `traffic-escape.bundle` preserves the original and changed commits for import into a personal repository. `changes.patch` preserves the same commit sequence as mail patches.

The original assignment repository has not been modified and no upstream pull request was opened.
