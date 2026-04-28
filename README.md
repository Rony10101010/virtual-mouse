# 🖱️ Virtual Mouse — Gesture-Controlled Mouse via Webcam

Control your computer mouse using hand gestures captured through a webcam. No hardware required beyond a standard camera.

---

## Description

Virtual Mouse uses computer vision and hand landmark detection to translate real-time hand gestures into mouse actions — move, click, double-click, right-click, and drag. Built on MediaPipe and OpenCV, it processes webcam frames to detect finger positions and maps them to screen coordinates. A Tkinter GUI provides a simple launcher interface.

---

## Features

- **Mouse movement** — index finger alone moves cursor across screen
- **Left click** — index finger + pinky raised
- **Double click** — pinky only raised
- **Click-and-drag** — all five fingers raised; hold to drag
- **Right click** — thumb + pinky raised
- **Smoothing** — exponential interpolation reduces jitter
- **FPS display** — live frame rate shown in camera window
- **GUI launcher** — Tkinter window to start control and view gesture reference

---

## Project Structure

```
mouse-project/
├── hand_tracking_module.py   # HandDetector class: landmark detection, finger state, distance
├── main.py                   # Core control loop: gesture → mouse action mapping
└── ui.py                     # Tkinter GUI: launcher + gesture cheat sheet
```

### Module Responsibilities

| File | Role |
|------|------|
| `hand_tracking_module.py` | Wraps MediaPipe Hands; exposes `find_hands()`, `find_position()`, `fingers_up()`, `find_distance()` |
| `main.py` | Reads webcam, calls detector, maps finger states to `autopy`/`pyautogui` mouse actions |
| `ui.py` | Tkinter front-end; runs `main.start_mouse_control()` in a daemon thread |

---

## Installation

### Prerequisites

- Python 3.8–3.10 (MediaPipe has limited Python 3.11+ support)
- Webcam

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/virtual-mouse.git
cd virtual-mouse

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install opencv-python mediapipe numpy autopy pyautogui
```

> **Note (macOS):** `autopy` requires Rust toolchain to build. Install via `brew install rust` first.  
> **Note (Linux):** May require `python3-tk` for the GUI (`sudo apt install python3-tk`).

---

## Usage

### GUI mode (recommended)

```bash
python ui.py
```

Click **Start** to begin gesture tracking. Press `ESC` in the camera window to stop.

### Headless mode

```bash
python main.py
```

Runs the control loop directly with no launcher window.

---

## Gesture Reference

| Gesture | Action |
|---------|--------|
| Index finger only | Move mouse |
| Index + Pinky | Left click |
| Pinky only | Double click |
| All fingers up | Click and drag |
| Thumb + Pinky | Right click |

---

## Configuration

Tunable constants in `main.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `cam_width` | `1280` | Webcam capture width |
| `cam_height` | `720` | Webcam capture height |
| `frame_margin` | `10` | Dead-zone margin around frame edges |
| `smooth_factor` | `7` | Higher = smoother but more lag |
| `click_cooldown` | `0.6` | Seconds between registered clicks |

Detection confidence thresholds in `HandDetector` instantiation (`main.py`):

```python
detector = HandDetector(detection_con=0.8, max_hands=1)
```

---

## Dependencies

| Library | Purpose |
|---------|---------|
| `opencv-python` | Webcam capture and frame rendering |
| `mediapipe` | Hand landmark detection (21 keypoints) |
| `numpy` | Coordinate interpolation |
| `autopy` | Low-level mouse move and button toggle |
| `pyautogui` | Click and double-click actions |
| `tkinter` | GUI launcher (stdlib) |

---

## Known Limitations

- `autopy` is not actively maintained and may fail to install on Python 3.11+
- Thumb detection uses horizontal axis only — may misfire on rotated hands
- Right-click gesture conflicts with drag-release if fingers change order quickly
- No gesture for scroll

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please keep PRs focused and include a brief description of what changed and why.

---

## License

[MIT License](LICENSE) — or replace with your chosen license.
