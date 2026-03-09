from database import setup_database
from loader import load_data
from graph_builder import build_graph, draw_graph


def main():

    setup_database()
    load_data()
    graph = build_graph()
    draw_graph(graph)


if __name__ == "__main__":
    main()