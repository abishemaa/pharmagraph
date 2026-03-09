from database import init_db
from cli import run_cli

if __name__ == "__main__":
    # Init DB if not exists
    init_db()
    # Start CLI
    run_cli()