from __future__ import division
from collections import namedtuple
import random

random.seed(1234)

Player = namedtuple('Player', ['at_bats', 'outs', 'singles', 'doubles', 'triples', 'home_runs'])

at_bat_outcome_dict = {
    'out': 0,
    '1b' : 1,
    '2b' : 2,
    '3b' : 3,
    'hr' : 4
}


def get_at_bat_outcome(player, key):
    if player.outs >= key:
        return at_bat_outcome_dict['out']
    elif player.outs + player.singles >= key:
        return at_bat_outcome_dict['1b']
    elif player.outs + player.singles + player.doubles >= key:
        return at_bat_outcome_dict['2b']
    elif player.outs + player.singles + player.doubles + player.triples >= key:
        return at_bat_outcome_dict['3b']
    elif player.outs + player.singles + player.doubles + player.triples + player.home_runs >= key:
        return at_bat_outcome_dict['hr']
    print "Error: Got bad key for player"


def at_bat(player):
    key = random.randrange(1, player.at_bats)
    return get_at_bat_outcome(player, key)


def add_runs(basepath_state):
    runs = 0

    if basepath_state >= 64:
        runs += 1
        basepath_state += -64

    if basepath_state >= 32:
        runs += 1
        basepath_state += -32

    if basepath_state >= 16:
        runs += 1
        basepath_state += -16

    if basepath_state >= 8:
        runs += 1
        basepath_state += -8

    return basepath_state, runs


def get_player(lineup, player_index):
    return lineup[player_index]


def run_inning(lineup, player_index):
    basepath_state = 0
    outs = 0
    runs = 0

    while outs < 3:
        player = get_player(lineup, player_index % 9)
        at_bat_outcome = at_bat(player)
        if at_bat_outcome == at_bat_outcome_dict['out']:
            outs += 1
        else:
            basepath_state = basepath_state << at_bat_outcome
            basepath_state += (2 ^ (at_bat_outcome - 1))
            basepath_state, new_runs = add_runs(basepath_state)
            runs += new_runs

        player_index += 1

    return runs, player_index % 9


def run_game(lineup):
    runs = 0
    inning = 1
    player_index = 0

    while inning <= 9:
        new_runs, player_index = run_inning(lineup, player_index)
        runs += new_runs
        inning += 1

    return runs


def iterate_games(lineup, total_iterations):
    iterations_run = 0
    score_total = 0

    while iterations_run < total_iterations:
        if iterations_run % (total_iterations / 10) == 0 and iterations_run != 0:
            print "Iterations: " + str(iterations_run)
        score_total += run_game(lineup)
        iterations_run += 1

    runs_per_game = score_total / total_iterations

    runs_per_season = runs_per_game * 132

    print "Total runs: " + str(score_total) + " RPG: " + str(runs_per_game) + " RPS " + str(runs_per_season)
    return runs_per_game


def significance_validator():
    roster = [
        Player(678, 416, 200, 34, 11, 17),
        Player(616, 313, 218, 51, 16, 18),
        Player(613, 366, 205, 21, 8, 13),
        Player(609, 370, 202, 23, 6, 8),
        Player(572, 354, 185, 24, 6, 3),
        Player(566, 338, 176, 29, 10, 13),
        Player(522, 333, 138, 28, 11, 12),
        Player(289, 196, 77, 7, 6, 3),
        Player(263, 167, 69, 12, 7, 8)
    ]
    iterations = 1
    print "Constructed roster, starting iterations."
    while iterations > 0:
        iterate_games(roster, 5000000)
        iterations -= 1

print "Running significance validator"
significance_validator()

