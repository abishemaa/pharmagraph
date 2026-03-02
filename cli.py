# Command-line interface
from models import list_drugs, get_interactions

def main():
    print("=== PharmaGraph v1 CLI ===")
    print("Available drugs:", ", ".join(list_drugs()))
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Enter a drug to see interactions: ").strip()
        if query.lower() == "exit":
            break

        if query not in list_drugs():
            print(f"{query} not found. Try again.\n")
            continue

        interactions = get_interactions(query)
        if not interactions:
            print(f"No interactions found for {query}.\n")
            continue

        print(f"\nInteractions for {query}:")
        for item in interactions:
            print(f"- {item['drug']} | Severity: {item['severity']} | Mechanism: {item['mechanism']}")
        print("")  # extra line for readability

if __name__ == "__main__":
    main()