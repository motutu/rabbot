# I just frigging want to use new features, yet xenial always holds me back.

import random


if not hasattr(random, 'choice'):
    def random_choice(seq):
        try:
            return random.sample(seq, 1)[0]
        except ValueError:
            raise IndexError

    random.choice = random_choice
