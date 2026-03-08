function loadGraph() {

    const drug = document.getElementById("drug").value;

    fetch(`/graph?drug=${drug}`)
    .then(r => r.json())
    .then(data => {

        const cy = cytoscape({

            container: document.getElementById('cy'),

            elements: [
                ...data.nodes,
                ...data.edges
            ],

            style: [
                {
                    selector: 'node',
                    style: {
                        'label': 'data(label)'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 2
                    }
                }
            ],

            layout: {
                name: 'cose'
            }
        });

    });
}