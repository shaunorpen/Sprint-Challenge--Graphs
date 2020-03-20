from room import Room
from player import Player
from world import World

from util import Queue, Stack

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

traversal_path = list()

def build_graph(player):
    q = Queue()
    graph = dict()
    visited = set()

    q.enqueue(player.current_room)

    while q.size() > 0:
        current_room = q.dequeue()
        next_rooms = [(exit, getattr(current_room, f'{exit}_to')) for exit in ['n', 's', 'e', 'w']]
        exits = dict()
        for (direction, room) in next_rooms:
            if room is not None:
                exits[direction] = room.id
                if room not in visited:
                    q.enqueue(room)
        visited.add(current_room)
        graph[current_room.id] = exits
    
    return graph

graph = build_graph(player)

def generate_possible_path(graph, player):
    explored = set()

    def explore(graph, player):
        path = list()

        unexplored_exits = [exit for exit in graph[player.current_room.id] if graph[player.current_room.id][exit] not in explored]
        
        while len(unexplored_exits) > 0:
            explored.add(player.current_room.id)
            direction = random.choice(unexplored_exits)
            path.append(direction)
            player.travel(direction)
            unexplored_exits = [exit for exit in graph[player.current_room.id] if graph[player.current_room.id][exit] not in explored]

        explored.add(player.current_room.id)

        return path

    def path_to_nearest_unexplored(graph, player):
        q = Queue()
        visited = set()
        exits = graph[player.current_room.id]
        for exit in exits:
            q.enqueue([exit])

        while q.size() > 0:
            path = q.dequeue()
            current_room = player.current_room.id
            for step in path:
                current_room = graph[current_room][step]
            visited.add(current_room)
            if current_room not in explored:
                for direction in path:
                    player.travel(direction)
                return path
            else:
                exits = graph[current_room]
                for exit in exits:
                    if graph[current_room][exit] not in visited:
                        q.enqueue([*path, exit])
        
        return list()


    while len(explored) < len(graph):
        traversal_path.extend(explore(graph, player))
        traversal_path.extend(path_to_nearest_unexplored(graph, player))

generate_possible_path(graph, player)

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