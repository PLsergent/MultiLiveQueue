---
description: Queue commands for matchmaking
---

# Queue commands

There are 3 different types of matchmaking queues:

* Casual queue
* Ranked: captain queue
* Ranked: random queue

The difference are explained in the following section (click to know more)

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Casual queue</strong></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f389">🎉</span></td><td>You can play against anyone and the result will not change your ranking points</td><td><a href="casual.md">casual.md</a></td></tr><tr><td><strong>Captain queue</strong></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f38c">🎌</span> ranked</td><td>A captain will be selected, he can then choose a teammate. It has effects on your ranking points</td><td><a href="rank-queue/captain-queue.md">captain-queue.md</a></td></tr><tr><td><strong>Random queue</strong></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f4a6">💦</span> ranked</td><td>The players in the queue will randomly be put in two teams. It has effects on your ranking points</td><td><a href="rank-queue/random-queue.md">random-queue.md</a></td></tr></tbody></table>

## casual

{% code title="to join the casual queue" %}
```
/queue casual
```
{% endcode %}

## ranked captain\_queue

{% code title="to join a captain ranked queue" %}
```
/queue ranked captain_queue
```
{% endcode %}

## ranked random\_queue

{% code title="to join a random ranked queue" %}
```
/queue ranked random_queue
```
{% endcode %}

## status

{% code title="display current queue status" %}
```
/queue status
```
{% endcode %}

## leave

{% code title="leave your current queue" %}
```
/queue leave
```
{% endcode %}

## empty\_all\_queues :warning:

{% hint style="info" %}
Admin command only
{% endhint %}

{% code title="empty all queues" %}
```
/queue empty_all_queues
```
{% endcode %}

## kick :warning:

{% hint style="info" %}
Admin command only
{% endhint %}

{% code title="kick a player from his queue" %}
```
/queue kick <username>
```
{% endcode %}
