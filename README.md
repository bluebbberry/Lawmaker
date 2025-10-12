# Law Maker

First-order-logic-based Zacktronic-like point'n' click game. Here is a short [demo](https://youtu.be/sGs8lp9hefo?si=j5nnadeRBm_LTJku).

## Requirements

- Python 3.8+
- SWI-Prolog 8.0+ (with Janus support)
- Tkinter (usually included with Python)

## Installation

### 1. Install SWI-Prolog

**macOS:**
```bash
brew install swi-prolog
```

**Ubuntu/Debian:**

See [here](https://www.swi-prolog.org/build/unix.html).

**Windows:**
- Download from https://www.swi-prolog.org/download/stable
- Install with default options

### 2. Install Python Dependencies

Create a python virtual environment, source it, then:

```bash
pip install janus-swi pillow
```

**Note:** `janus-swi` requires SWI-Prolog to be installed first.

## Running the Game

```bash
python main.py
```

## Troubleshooting

**"janus_swi not available"**
- Ensure SWI-Prolog is installed first
- Try: `pip install --upgrade janus-swi`
- Verify SWI-Prolog: `swipl --version`

**"No levels could be loaded"**
- The game creates sample levels automatically on first run
- Check that `levels/` directory exists

**Tkinter missing**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (usually pre-installed)
# Reinstall Python from python.org if needed
```

## Creating Custom Levels

Add JSON files to the `levels/` directory. See `levels/01_student_meal_subsidy.json` for the format.

## License

MIT License, created by Jan Bingemann
