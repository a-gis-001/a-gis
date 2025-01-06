def _extract_thread(*, conversations, entry, model="qwq:latest"):
    """Extract a thread from the conversations.

    conversations: the input list of conversations
    entry: the index in conversations in the thread

    """
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Code.make_struct
    import numpy

    def extract_indices(text):
        import re

        pattern = r"parts:\s*([0-9, \-]+)"
        match = re.search(pattern, text.lower())

        indices = []
        if match:
            indices_str = match.group(1)
            indices = [int(x.strip()) for x in indices_str.split(",")]
        indices.append(0)
        indices = sorted(set(indices))
        return indices

    chatbot = A_GIS.Ai.Chatbot.init(
        model=model,
        num_ctx=10000,
        num_predict=10000,
        mirostat=2,
        temperature=0.5,
        system=f"""You will be shown a conversation on a messaging app split
into 'Parts'. Each part belongs to one 'thread'. There may be multiple 'threads' in the
conversation, for example someone is talking about a problem compiling and someone else
is asking about how to login to a specific machine.
The parts will be numbered sequentially by timestamp with your goal being to
determine which parts of the conversation are in the same thread as Part 0.
Note, the same user may be contributing to different threads.
Also, some users make smaller messages quicker instead of typing a long messages.
Take into account the timestamps when deciding if a user is adding to a
previous message in the same thread or participating in another thread.
If the time difference between messages is more than a few hours, it is usually
a new thread.

For example, you will receive:

    ## Part -2
    UserA: Does anyone know a good place for lunch?

    ## Part -1
    UserA: Also, how many nodes does Helios have?

    ## Part 0
    UserB: I like Buddy's BBQ.

    ## Part 1
    UserC: 63

    ## Part 2
    UserD: Are you sure? I think it's 75.

    ## Part 3
    UserA: Thanks!

You will then output the parts which are in the same thread as Part 0 verbatim.

    ## Part -2
    UserA: Does anyone know a good place for lunch?

    ## Part 0
    UserB: I like Buddy's BBQ.

    ## Part 3
    UserA: Thanks!

You will then give an explanation why they are in the same thread.

    UserA asks about lunch and UserB answers with a well-known restaurant. UserA responds quickly with Thanks.

Finally, you will end with a single line with "PARTS:", followed by listing the comma separated
part numbers of the thread which includes Part 0. For example:

    PARTS: -2,0,3

Note, part 0 should always be in the list.
    """
    )

    text = ""
    for i, f in enumerate(conversations):
        text += "\n## Part " + str(i - entry) + "\n" + f + "\n"
    text +="---\nRemember that the your final line must be 'PARTS:', followed by the comma-separated parts of the thread related to part 0. Part 0 should always in the list."
    print(text)
    r = chatbot.chat(message=text)
    x = r.response["message"]["content"]
    print('---')
    print(x)
    print('---')
    o_indices = extract_indices(x)
    print('PARTS:',o_indices)
    indices = numpy.array(o_indices) + entry

    return A_GIS.Code.make_struct(
        text=text, o_indices=o_indices, indices=indices, response=x
    )
