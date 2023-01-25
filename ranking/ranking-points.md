---
description: Ranking points explained
---

# Ranking points

## Ranking points

After each game, you'll win or lose points depending on the results of the match.

More on that here :thumbsup:

{% content-ref url="../match/points-calculation.md" %}
[points-calculation.md](../match/points-calculation.md)
{% endcontent-ref %}

The ranks have been divided in 5 sections: **S**, **A**, **B**, **C**, **D**, obviously the rank S being the better and D being the worst.

{% hint style="info" %}
The ranks could change depending on the amount of player
{% endhint %}

When you start using the bot you'll have 0 ranking points, rank D.

{% hint style="info" %}
Note that you cannot go bellow 0 points
{% endhint %}

To access a new rank you need to have a minimum of X points being:

* 100 points for **S**
* 75 points for **A**
* 50 points for **B**
* 25 points for **C**
* 0 points for **D**

> I have 52 ranking point, then I'm in **A** rank.

## Ranking file

All the rank will be stored in a Json file like this:

```json
{
    "S": {
        "min_points": 100,
        "players": []
    },
    "A": {
        "min_points": 75,
        "players": []
    },
    "B": {
        "min_points": 50,
        "players": []
    },
    "C": {
        "min_points": 25,
        "players": []
    },
    "D": {
        "min_points": 0,
        "players": [
            "PL / Aikawa Towa#5031"
        ]
    }
}
```
