---
description: Captain queue explained
---

# Captain queue

{% code title="command to join a captain ranked queue" %}
```
/queue ranked captain_queue
```
{% endcode %}

## Principles

The **captain ranked queue** will match you with any players that joined the queue **within your rank**. As a result, the result of the match will be reflected on your ranking points.

## Queue

The bot will match **the first 4 players** that will join the queue within your rank. They will then be removed from the queue.

## Teams

When a match is found, the bot will select a **captain,** this player will then **have to pick** an available player from the 3 others that were in the queue. The selected player will be the captain's teammate, the other 2 players will be put in the other team. At this moment the channels will be created.
