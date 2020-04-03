
import Combinatorics

struct Player
    at_bats::Int
    outs::Int
    singles::Int
    doubles::Int
    triples::Int
    home_runs::Int
end

@enum AtBatOutcome out=0 single=1 double=2 triple=3 home_run=4


function get_at_bat_outcome(player::Player, key::Int)
    if player.outs >= key
        # println("Got out")
        return out
    elseif player.outs + player.singles >= key
        # println("Got single")
        return single
    elseif player.outs + player.singles + player.doubles >= key
        # println("Got double")
        return double
    elseif player.outs + player.singles + player.doubles + player.triples >= key
        # println("Got triple")
        return triple
    elseif player.outs + player.singles + player.doubles + player.triples + player.home_runs >= key
        # println("Got homer")
        return home_run
    end
    at_bats = player.at_bats
    println("Error: Got key $key for player with at bats $at_bats")
    throw(DomainError())
end


function at_bat(player::Player, rng)
    key::Int = rand(rng, 1:player.at_bats)
    return get_at_bat_outcome(player, key)
end


function add_runs(basepath_state::Int)
    runs = 0
    if basepath_state >= 64
        # println("Scoring play: scored from third on homer")
        runs += 1
        basepath_state += -64
    end
    if basepath_state >= 32
        # println("Scoring play: scored from third on triple, second on homer")
        runs += 1
        basepath_state += -32
    end
    if basepath_state >= 16
        # println("Scoring play: scored from third on double, second on triple, first on homer")
        runs += 1
        basepath_state += -16
    end
    if basepath_state >= 8
        # println("Scoring play: scored from third on single, second on double, first on triple, home on homer")
        runs += 1
        basepath_state += -8
    end
    return basepath_state, runs
end


function get_player(lineup::Array{Player}, player_index::Int)
    return lineup[player_index+1]
end


function run_inning(lineup::Array{Player}, player_index::Int, rng)
    basepath_state::Int = 0
    outs::Int = 0
    runs::Int = 0

    while outs < 3
        player = get_player(lineup, player_index % 9)
        at_bat_outcome::AtBatOutcome = at_bat(player, rng)
        if at_bat_outcome == out
            outs += 1
        else
            basepath_state = basepath_state << Int(at_bat_outcome)
            basepath_state += (2 ^ (Int(at_bat_outcome) - 1))
            # println("Base state: $basepath_state")
            basepath_state, new_runs = add_runs(basepath_state)
            # println("Base state: $basepath_state")
            runs += new_runs
        end
        player_index += 1
    end
    # println("End inning")
    return runs, player_index % 9
end


function run_game(lineup::Array{Player}, rng)
    runs::Int = 0
    inning::Int = 1
    player_index::Int = 0

    while inning <= 9
        new_runs, player_index = run_inning(lineup, player_index, rng)
        runs += new_runs
        inning += 1
        # println("Runs: $runs, Inning: $inning")
    end

    return runs
end


function iterate_games(lineup::Array{Player}, total_iterations::Int, rng)
    iterations_run::Int = 0
    score_total::Int = 0

    while iterations_run < total_iterations
        if iterations_run % (total_iterations / 10) == 0 && iterations_run != 0
            println("Iterations: $iterations_run")
        end
        score_total += run_game(lineup, rng)
        iterations_run += 1
    end

    runs_per_game = score_total / total_iterations

    runs_per_season = runs_per_game * 162

    println("Total Runs: $score_total Runs Per Game: $runs_per_game Runs Per Season: $runs_per_season")
    return runs_per_game
end


function significance_validator()
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
    iterations::Int = 10
    rng = MersenneTwister(1234)
    while iterations > 0
        iterate_games(roster, 5_000_000, rng)
        iterations -= 1
    end
end

significance_validator()

