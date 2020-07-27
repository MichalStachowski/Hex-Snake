import random


class Apple:
    def __init__(self):
        self.x = None
        self.y = None
        self.is_ate = False

    def random_apple_pos(self, s1_pos, s2_pos):
        possible_action = ["even", "odd"]
        chosen_action = random.choice(possible_action)
        if chosen_action == "even":
            rand_x = random.randrange(0, 19, 2)
            rand_y = random.randrange(0, 19, 2)
        else:
            rand_x = random.randrange(1, 20, 2)
            rand_y = random.randrange(1, 20, 2)

        if [rand_x, rand_y] in s1_pos or [rand_x, rand_y] in s2_pos:
            pass
        else:
            self.x = rand_x
            self.y = rand_y
