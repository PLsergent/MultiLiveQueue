---
description: How many ranking points can I win or lose?
---

# Points calculation

## Principles

At the end of a ranked match, once one of the players reported the match, the ranking points will be updated. The ranking points won/lost after a match depends on 2 factors:

* Difference between the KOs of the two teams (if one game) / or difference between the games won (if BO match)
* Win streak multiplier

{% hint style="info" %}
Note that you can't go bellow 0 ranking points.
{% endhint %}

You always start with 0 points.

## Calculation

1. Difference between&#x20;
   * Your KOs and enemy team KOs (if one game)
   * OR
   * Number of games you won and number of games won by the enemy (if BO match)
2. Multiply the difference with your win streak multiplier (only when winning)

$$
points\_gained = difference * multiplier
$$

## Examples

<details>

<summary>Winning scenario</summary>

You won your match 4-2, then you report the result this way:

```
/match report win 4-2
```

The points difference is **2**.

You had a win streak multiplier of **1.4,** you then do: **2 \* 1.4 = 2.8**

The win streak multiplier is increased by 0.2 for the next game.

:tada:**You won 2.8 ranking points.**&#x20;

</details>

<details>

<summary>Losing scenario</summary>

You lost your match 1-4, then you report the result this way:

```
/match report win 1-4
```

The points difference is **3**.

The win streak multiplier is reset to 1.

****:cry: **You lost 3 ranking points.**&#x20;

</details>

## Win streak multiplier

In order to reward the players that are winning a lot of games in a row, the bot has a win streak multiplier system. Meaning, each time you win, you'll gain a little bit more points. If you lose, the multiplier will be reset to 1.

* Win: increase win streak multiplier by **0.2**
* Loss: reset win streak multiplier to **1**

{% hint style="info" %}
If you win a match the multiplier will be taken into account. If you lose the multiplier is not taken into account.
{% endhint %}
