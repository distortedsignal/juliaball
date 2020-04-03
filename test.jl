
using Base.Test
using Game

player = Player(678, 416, 200, 34, 11, 17)

@test Int(get_at_bat_outcome(player, 1)) == 0
