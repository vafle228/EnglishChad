from ChadUtils.notifier import notifySubscribers
from ChadUtils.subscriber import ChadSubscriber, Subscriptions

ChadSubscriber.addNewSubsciber(Subscriptions.SOLUTION_ADD, notifySubscribers)
