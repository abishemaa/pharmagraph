from graph.visualizer import visualize_graph


def run_cli():
    print("Welcome to PharmaGraph CLI")
    print("Type a drug name to see interactions, 'all' for full network, 'exit' to quit.")

    while True:
        cmd = input("Enter drug name > ").strip()
        if cmd.lower() == 'exit':
            break
        elif cmd.lower() == 'all':
            visualize_graph()
        elif cmd:
            visualize_graph(cmd)
        else:
            print("Please enter a valid drug name.")