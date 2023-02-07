---
description: Match commands to report the results
---

# Match commands

Once a match has started, each team will have a **dedicated voice and text channel** that them and only them can access.

## report

Inputs:

* **result** of the match for you, either "win" or "loss"
* **score** of the match, always from **your perspective** meaning, you lost, the enemy have 4 KOs and you have 2, then you'll input "2-4" (you can also refer to the score as a BO match with several games, for instance you won 2 games to 1 in the match then enter "2-1")

{% code title="to report a match with result and score" %}
```
/match report <win-loss> <score>
```
{% endcode %}

Effects: once one of the players reported the match

* Ranking points updated
* Rank updated (if needed)
* Players removed from the match > they can join a queue again
* Match delete
* Channels deleted

## pick

_Needed when you've been selected as a captain in a captain queue_

Inputs:

* **teammate** name that you select (help with autocomplete to see the available players)

{% code title="to pick a teammate from the available players" %}
```
/match pick <username>
```
{% endcode %}

Effects:

* The selected player will join your team
* The remaining player will be put in the same team
* The voice and text channels will be created

## abandon

_Do not abuse this command, it has to be used only when one of the players that was in a queue happened to not be available when the match starts._

{% code title="to abandon a match" %}
```
/match abandon
```
{% endcode %}

Effects:

* The player will be removed from the available players and/or from the team of the match, as a result, if the match is still reported this will have no effects on the player ranking points.&#x20;
* If the match has no more players in it, then the match will be deleted. As a result, all the players have to abandon a match for the match to be deleted. This has been made to prevent abuses.&#x20;

## delete\_channels :warning:

{% hint style="info" %}
Admin command only
{% endhint %}

{% code title="to delete all match channels still opened" %}
```
/match delete_channels
```
{% endcode %}

This command has been made to delete all channels created by matches in case of a bug.
