from data import repositories

class InteractionService:
    def __init__(self):
        pass  # No state needed yet, could add caching later

    def get_interactions(self, drug_name):
        """
        Returns structured interactions for a given drug.
        Output example:
        [
            {
                "drug": "Aspirin",
                "severity": "Severe",
                "mechanism": "Bleeding risk"
            }
        ]
        """
        drug = repositories.get_drug_by_name(drug_name)
        if not drug:
            return []

        interactions_raw = repositories.get_interactions_for_drug(drug[0])  # assuming drug[0] is ID
        interactions = []

        for row in interactions_raw:
            # Map DB columns to structured output
            interactions.append({
                "drug": drug[1],           # name
                "severity": row[2],        # severity column in interactions table
                "mechanism": row[3],       # mechanism column
            })

        return interactions

    def get_all_drugs(self):
        """
        Returns list of all drugs (names only for now)
        """
        drugs_raw = repositories.get_all_drugs()
        return [row[1] for row in drugs_raw]  # assuming row[1] is name