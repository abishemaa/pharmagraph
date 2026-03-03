from database import init_db
from seed_data import seed_database
from cli import run_cli

if __name__ == "__main__":
    # Init DB if not exists
    init_db()
    # Seed sample data
    seed_database()
    # Start CLI
    run_cli()