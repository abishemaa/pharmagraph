#main.py
from database import setup_database
from loader import load_data
from cli import run_cli

def main():
    setup_database()
    load_data()
    run_cli()

if __name__ == "__main__":
    main()