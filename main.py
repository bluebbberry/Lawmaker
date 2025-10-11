#!/usr/bin/env python3
"""
Law Maker - A Prolog Programming Game
Minimalist pastel aesthetic with quietly utopian undertones.
View-based navigation for immersive gameplay.
"""

import os
from src.level_loader import LevelLoader
from src.law_maker_gui import LawMakerGUI

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import janus_swi as janus
    JANUS_AVAILABLE = True
except ImportError:
    JANUS_AVAILABLE = False


def create_sample_levels():
    """Create sample level files"""
    LevelLoader.create_sample_levels("levels")
    print("Sample tasks created in 'levels' directory")


def main():
    """Main entry point"""
    print("Initializing Law Maker...")

    if not os.path.exists("levels") or not os.listdir("levels"):
        print("Setting up task database...")
        create_sample_levels()

    if not JANUS_AVAILABLE:
        print("Warning: janus_swi not available")
        print("Install with: pip install janus_swi")

    try:
        print("Launching interface...")
        app = LawMakerGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nShutdown initiated.")
    except Exception as e:
        print(f"System error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
