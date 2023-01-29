---
description: MultiLiveQueue starting point
---

# 🤸 Start here

## Welcome

Thanks for using MultiLiveQueue, once installed on your server you can directly start using the commands. The first command you'll enter will register you as a user in the bot's data files.

{% hint style="info" %}
First command = user registered
{% endhint %}

## First steps

You can add your Multiversus username so your teammates and opponent can easily find you ingame.

{% hint style="info" %}
You have to set your ingame username to join a matchmaking queue :eyes:
{% endhint %}

{% code title="add ingame username" %}
```
/user ingame Holapapalouis
```
{% endcode %}

You can also get your **Muliversus** link with the following command.

{% code title="get muliversus link" %}
```
/user muliversus
```
{% endcode %}

> [https://muliversus.plsergent.xyz/Holapapalouis](https://muliversus.plsergent.xyz/Holapapalouis)

Then you're ready to queue, note that you can access your stats at any time with:

```
/user stats
```

## Queuing

You're now ready to join a matchmaking queue! To do so, use the **/queue** commands.

{% hint style="info" %}
Note that you can't join a queue if you're in a match or already in an other queue :no\_entry:
{% endhint %}

{% code title="queue commands" %}
```
/queue casual
/queue ranked captain_queue
/queue ranked random_queue
```
{% endcode %}

{% code title="leave current queue" %}
```
/queue leave
```
{% endcode %}

More about the queue commands here: [Broken link](broken-reference "mention")

## Match

Once enough player has been found to start a match, you'll get a message, and the match category and text/voice channels will be created for your team.

{% hint style="info" %}
Note that the channels created are only accessible for your team and will be deleted after the match result is reported :warning:
{% endhint %}

The main command is to report the result of the match. This can be done by the winner or loser side.

{% code title="report match if won" %}
```
/match report win 4-2
```
{% endcode %}

{% code title="report match if you lost" %}
```
/match report loss 2-4
```
{% endcode %}

More about the match here: [Broken link](broken-reference "mention")
