import sys
import A_GIS.Conversation.Slack.extract_threads
import networkx
import matplotlib.pyplot as plt

directory=sys.argv[1]
channel = sys.argv[2]
date = sys.argv[3]

x = A_GIS.Conversation.Slack.extract_threads(
        directory=directory,
        channel=channel,
        date=date,
        only_entry=0
    )

g = x.graph

# Get the connected components of the undirected version of the graph
connected_components = list(networkx.connected_components(g.to_undirected()))

# Map each node to its cluster ID
cluster_map = {node: i for i, component in enumerate(connected_components) for node in component}

# Assign colors to nodes based on their cluster
colors = [cluster_map[node] for node in g.nodes()]

# Visualize the graph with cluster-based colors
pos = networkx.spring_layout(g.to_undirected(), k=1.0, seed=33)
networkx.draw(g, pos, with_labels=True, node_color=colors, node_size=300, cmap=plt.cm.rainbow, arrows=False)
edge_weights = [d['weight'] for u, v, d in g.edges(data=True)]
networkx.draw_networkx_edges(g, pos, width=edge_weights, arrows=False)
plt.show()
