from cli import commands

def run_cli():
    print("Welcome to PharmaGraph CLI")
    while True:
        cmd = input("Enter command (list, show <drug>, graph <drug>, exit): ").strip()
        if cmd == "exit":
            break
        elif cmd == "list":
            commands.list_drugs()
        elif cmd.startswith("show "):
            drug = cmd.split(" ", 1)[1]
            commands.show_interactions(drug)
        elif cmd.startswith("graph "):
            drug = cmd.split(" ", 1)[1]
            commands.visualize_interactions(drug)
        else:
            print("Unknown command")