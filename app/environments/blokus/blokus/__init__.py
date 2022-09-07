from gym.envs.registration import register

register(
    id='Blokus-v0',
    entry_point='blokus.envs:BlokusEnv',
)


