let Graph;

function loadGraph() {

    const drugInput = document.getElementById("drug");
    const drug = drugInput ? drugInput.value.trim() : "";

    fetch(`/graph?drug=${drug}`)
    .then(r => r.json())
    .then(data => {

        const nodes = data.nodes.map(n => ({ id: n.id }));
        const links = data.links.map(e => ({
            source: e.source,
            target: e.target
        }));

        if (!Graph) {
            Graph = ForceGraph3D()(document.getElementById('3d-graph'))
                .nodeLabel('id')
                .nodeAutoColorBy('id');
        }

        Graph.graphData({ nodes, links });

    })
    .catch(err => console.error("Graph load error:", err));
}

window.onload = loadGraph;