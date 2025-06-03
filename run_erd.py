import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the ERD creation
from assets.create_erd import create_erd

if __name__ == "__main__":
    create_erd()
    print("ERD created successfully! Check assets/erd_new.png")
