import sys
import A_GIS.Conversation.Slack.load_data

directory=sys.argv[1]
channel = sys.argv[2]
date = sys.argv[3]

x = A_GIS.Conversation.Slack.load_data(
        directory=directory,
        channel=channel,
        date=date
    )

for n in x.prev:
    print(f"- {n}")
for n in x.this:
    print(f"- {n}")
for n in x.next:
    print(f"- {n}")
