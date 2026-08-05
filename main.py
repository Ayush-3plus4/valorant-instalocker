import sys
import os
from detector import InstalockDetector
from gui import ValorantHUDGUI

def main():
    detector = InstalockDetector()
    app = ValorantHUDGUI(detector)
    app.mainloop()

if __name__ == "__main__":
    main()
