def extract_threads(
    *,
    directory,
    date,
    channel="random",
    adjacent_range=[-0.5, 0.5],
    only_entry=None,
    model="qwq:latest",
):
    """Extract the threads from a Slack export directory."""
    import A_GIS.Conversation.Slack.load_data
    import A_GIS.Conversation.Slack._extract_thread
    import networkx

    x = A_GIS.Conversation.Slack.load_data(
        directory=directory,
        channel=channel,
        date=date,
        adjacent_range=adjacent_range,
    )

    messages = x.prev
    i = len(messages)
    messages.extend(x.this)
    messages.extend(x.next)

    conversations = [f"[{ts}] {user}: {text}" for ts, user, text in messages]

    entries = [h for h in range(i, i + len(x.this))]
    if only_entry is not None:
        entries = [entries[only_entry]]

    groups = []
    for entry in entries:
        y = A_GIS.Conversation.Slack._extract_thread(
            conversations=conversations, entry=entry, model=model
        )
        groups.append(y)

    def add_node(graph, node_id, **attributes):
        """Add a node to the graph."""
        graph.add_node(node_id, **attributes)

    def add_connection(graph, source, target, weight_increment=1):
        """Add a directional connection or increment its weight."""
        if graph.has_edge(source, target):
            graph[source][target]["weight"] += weight_increment
        else:
            graph.add_edge(source, target, weight=weight_increment)

    graph = networkx.DiGraph()

    # Go through and create nodes for any single index groups.
    for group in groups:
        if len(group.indices) == 1:
            add_node(graph, group.indices[0], weight=1)

    # Go through and add connections.
    for group in groups:
        for i in range(len(group.indices) - 1):
            add_connection(
                graph,
                group.indices[i],
                group.indices[i + 1],
                weight_increment=1,
            )

    return A_GIS.Code.make_struct(
        messages=messages,
        conversations=conversations,
        graph=graph,
        groups=groups,
    )
