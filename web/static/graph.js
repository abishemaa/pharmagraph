function loadGraph() {

    const drug = document.getElementById("drug").value || "";

    fetch(`/graph?drug=${drug}`)
    .then(r => r.json())
    .then(data => {

        const nodes = data.nodes.map(n => ({ id: n.data.id }));
        const links = data.edges.map(e => ({
            source: e.data.source,
            target: e.data.target
        }));

        const Graph = ForceGraph3D()
            (document.getElementById('3d-graph'))
            .graphData({ nodes, links })
            .nodeLabel('id')
            .nodeAutoColorBy('id');

    });
}

window.onload = loadGraph;