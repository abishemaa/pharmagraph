let Graph = null;

function loadGraph() {

    const input = document.getElementById("drug");
    const drug = input ? input.value.trim() : "";

    const url = drug ? `/graph?drug=${drug}` : "/graph";

    fetch(url)
        .then(r => r.json())
        .then(data => {

            if (!Graph) {

                Graph = ForceGraph()(document.getElementById("graph"))
                    .nodeId("id")
                    .nodeLabel(node =>
                        `<b>${node.id}</b><br>
                        Class: ${node.class || "Unknown"}<br>
                        MOA: ${node.moa || "Unknown"}<br>
                        Metabolism: ${node.metabolism || "Unknown"}`
                    )
                    .nodeAutoColorBy("class")
                    .nodeRelSize(8)
                    .linkWidth(2);
            }

            Graph.graphData(data);

        })
        .catch(err => console.error(err));
}

window.onload = loadGraph;