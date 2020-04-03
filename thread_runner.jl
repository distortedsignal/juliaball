@everywhere include("game.jl")


function roster_permutation_generator_creator()
    first_value = 1

    function roster_permutation_generator()
        next_value = first_value
        first_value += 1
        if next_value > factorial(9)
            return 0
        else
            return next_value
        end
    end

    return roster_permutation_generator
end


function thread_permutation_generator_creator()
    first_value = 1

    function thread_permutation_generator()
        next_value = first_value
        first_value += 1
        if first_value == 9
            first_value = 1
        end
        return next_value
    end
    return thread_permutation_generator
end


roster_permutation_generator = roster_permutation_generator_creator()
thread_permutation_generator = thread_permutation_generator_creator()
ProcArray = Array{Any, 1}(8)

max_rpg = 0.0
best_roster = 0


permutation = roster_permutation_generator()
addprocs(8)

while permutation != 0
    thread_idx = thread_permutation_generator()
    ProcArray[thread_idx] = (permutation, remotecall(prepare_lineup_run_games, thread_idx+1, permutation, 5_000_000))

    if thread_idx == 8
        ProcResults = map(x -> (x[1], fetch(x[2])), ProcArray)
        for i in ProcResults
            if i[2] > max_rpg
                max_rpg = i[2]
                best_roster = i[1]
            end
        end
    end

    permutation = roster_permutation_generator()
end
# Procs = map(x -> remotecall(iterate_games, x, roster_permutation, 5_000_000), [2, 3, 4, 5, 6, 7, 8, 9])
# ProcResults = map(x -> fetch(x), Procs)
# final_rpg = sum(ProcResults) / length(ProcResults)
ProcIndicies = 2:9

Procs = map(x -> remotecall(prepare_lineup_run_games, x, permutation_generator(), 5_000_000), ProcIndicies)
ProcResults = map(x -> (x[1], fetch(x[2])), Procs)

println("Proc Results: $ProcResults")
