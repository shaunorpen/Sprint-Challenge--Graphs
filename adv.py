from room import Room
from player import Player
from world import World

from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
route = []

q = Queue()
q.enqueue((route, player.current_room))
visited = set()
routes = list()

while q.size() > 0:
    (route, current_room) = q.dequeue()
    next_rooms = [getattr(current_room, f'{exit}_to') for exit in ['n', 's', 'e', 'w']]
    unvisited_next_rooms = [room.id for room in next_rooms if room is not None and room.id not in visited]
    if len(unvisited_next_rooms) == 0:
        routes.append(route)
    else:
        for exit in current_room.get_exits():
            visited.add(current_room.id)
            next_room = getattr(current_room, f'{exit}_to')
            if next_room.id not in visited:
                q.enqueue(([*route, exit], next_room))

routes.sort(key=len)

traversal_path = []
substitutes = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

for i in range(len(routes)):
    if i < len(routes) - 1:
        forward = list(routes[i])
        backward = [substitutes[direction] for direction in forward[::-1]]
        traversal_path.extend(forward)
        traversal_path.extend(backward)
    else:
        traversal_path.extend(routes[i])

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
