import networkx as nx

class GraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def build_from_interactions(self, interactions_list):
        """
        interactions_list: list of dicts from InteractionService.get_interactions
        Example:
        [
            {"drug": "Aspirin", "severity": "Severe", "mechanism": "Bleeding risk"},
            ...
        ]
        """
        for inter in interactions_list:
            drug = inter["drug"]
            mech = inter["mechanism"]
            sev = inter["severity"]

            # Add node if missing
            if not self.graph.has_node(drug):
                self.graph.add_node(drug)

            # For demo: connect drug to mechanism as node, edge labeled with severity
            if not self.graph.has_node(mech):
                self.graph.add_node(mech)
            self.graph.add_edge(drug, mech, severity=sev)

        return self.graph