from classes.CTSP import CTSP
from classes.simple_objects.range import Range
from classes.simple_objects.position import Position
from classes.simple_objects.shape import Shape
from setup.environment_setup import Environment
import visualization.animate_2d


def square_shape_vertices(side_distance:float):
    # if increased efficiency is needed can be adapted to not check if time range is correct, although will cause
    # problems with quadtree parents not being added

    # array of positions of vertices for shape in order of x0, y0, x1, y1... where 0,0 is the center of the shape
    return [-1 * side_distance,
                  -1 * side_distance,
                  side_distance,
                  -1 * side_distance,
                  side_distance,
                  side_distance,
                  -1 * side_distance,
                  side_distance]

def rectangle_shape_vertices(side_distance:float):
    # if increased efficiency is needed can be adapted to not check if time range is correct, although will cause
    # problems with quadtree parents not being added

    # array of positions of vertices for shape in order of x0, y0, x1, y1... where 0,0 is the center of the shape
    return [-2 * side_distance,
                  -3 * side_distance,
                  side_distance,
                  -1 * side_distance,
                  side_distance,
                  side_distance,
                  -2 * side_distance,
                  side_distance]

def rectangle_shape_vertices2(side_distance:float):
    # if increased efficiency is needed can be adapted to not check if time range is correct, although will cause
    # problems with quadtree parents not being added

    # array of positions of vertices for shape in order of x0, y0, x1, y1... where 0,0 is the center of the shape
    return [-4 * side_distance,
                  -2 * side_distance,
                  side_distance,
                  -0.5 * side_distance,
                  side_distance,
                  side_distance,
                  -3 * side_distance,
                  side_distance]


temp_environment = Environment(Range(0, 400), Range(0, 400), 0.5)

# initialize model
model = CTSP(temp_environment)

# initialize arrays of positions for different agents
# positions = []
# for i in range(60, 20 - 1, -1):
#     positions.append(Position(i + 300, i + 200, 80 - i))
# model.add_agent_from_positions(positions, Shape(rectangle_shape_vertices2(10)))

positions = []
for i in range(30, 300 + 1):
    positions.append(Position(i, 350-i, i))
model.add_agent_from_positions(positions, Shape(rectangle_shape_vertices(20)))

positions = []
for i in range(50, 300 + 1):
    positions.append(Position(i, i, i))
model.add_agent_from_positions(positions, Shape(rectangle_shape_vertices2(30)))

# print out basic model information
# model.print_modal()

# visualize model
visualization.animate_2d.run_model(model, show_start=True, show_destination=True)