from classes.CTSP import CTSP
from classes.simple_objects.range import Range
from classes.simple_objects.position import Position
from classes.simple_objects.shape import Shape
import visualization.main

side_distance = 5
# array of positions of vertices for shape in order of x0, y0, x1, y1... where 0,0 is the center of the shape
shape_vertices = [-1 * side_distance,
                  -1 * side_distance,
                  side_distance,
                  -1 * side_distance,
                  side_distance,
                  side_distance,
                  -1 * side_distance,
                  side_distance]

# initialize model
model = CTSP(Range(0, 400), Range(0, 400))

# initialize arrays of positions for different agents
positions = []
for i in range(60, 20 - 1, -1):
    positions.append(Position(i + 300, i + 200, 80 - i))
model.add_agent_from_positions(positions, Shape(shape_vertices))

positions = []
for i in range(30, 50 + 1):
    positions.append(Position(i, i, i))
model.add_agent_from_positions(positions, Shape(shape_vertices))

positions = []
for i in range(10, 70 + 1):
    positions.append(Position(i, i + 100, i))
model.add_agent_from_positions(positions, Shape(shape_vertices))

# print out basic model information
# model.print_modal()

# visualize model
visualization.main.run_model(model, show_start=True, show_destination=True)
