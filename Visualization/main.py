from classes.agent import Agent
from classes.functionless.position import Position

from tkinter import *
import time


class VisualObject:

    # visual object initialization, where visualization is the specific tkinter polygon for this object
    def __init__(self, visual, agent: Agent, positions: [Position]):
        self.visual = visual
        self.agent = agent
        self.positions = positions


def run_model(model, show_start=False, show_destination=False):

    # declare tk object
    tk = Tk()

    # initialize canvas
    canvas_width = model.range_x.size()
    canvas_height = model.range_y.size()
    canvas = Canvas(tk, width=canvas_width, height=canvas_height)
    canvas.pack()

    # declare lists of objects that stores visualizations currently being shown in canvas
    visual_object_list = []

    # declare lists of objects that stores visualizations to be shown in canvas, these objects hold null values for
    # their visual property
    visual_object_list_to_add = []
    for agent in model.get_agents():
        temp_positions = agent.get_positions().copy()
        # reverse positions list as more efficient to remove from end of list
        temp_positions.reverse()

        # create object to store visualizations information
        to_add_visual_object = VisualObject(None, agent, temp_positions)
        visual_object_list_to_add.append(to_add_visual_object)

    # set constant variables
    time_var = model.quadtree.start_time
    time_label = canvas.create_text(canvas_width - 10, 10, text=("Time", time_var), font=("Comic Sans", 10))
    time_step = model.quadtree.time_step

    # loop through times in range of model
    for time_index in range(0, int((model.quadtree.end_time - model.quadtree.start_time)/time_step) + 1):
        # update time label
        canvas.itemconfig(time_label, text=time_var)

        # declare list to hold indexes objects removed during iteration of list, as it is not good to remove from lists
        # as they are iterated through
        pop_indexes = []
        for to_add_index in range(0, len(visual_object_list_to_add)):
            # check if visualization should be added to canvas
            if visual_object_list_to_add[to_add_index].agent.time_range.low_bound < time_var + time_step:
                agent = visual_object_list_to_add[to_add_index].agent

                # copy shape description list to ensure that original list is not mutated
                shape_starting_list = agent.get_shape().shape_vertices.copy()

                # add to x and y coordinates of shape description list agent's starting position to create shape
                # description list for visualization at specific position
                for index_x in range(0, len(shape_starting_list), 2):
                    shape_starting_list[index_x] = shape_starting_list[index_x] + agent.start_position.get_x()
                for index_y in range(1, len(shape_starting_list), 2):
                    shape_starting_list[index_y] = \
                        canvas_height - (shape_starting_list[index_y] + agent.start_position.get_y())

                # if start position indicators are on add start position polygon to screen
                if show_start:
                    canvas.create_polygon(shape_starting_list, fill="red")

                # if end position indicators are on add end position polygon to screen
                if show_destination:
                    shape_ending_list = agent.get_shape().shape_vertices.copy()
                    for index_x in range(0, len(shape_ending_list), 2):
                        shape_ending_list[index_x] = shape_ending_list[index_x] + agent.target_position.get_x()

                    for index_y in range(1, len(shape_ending_list), 2):
                        shape_ending_list[index_y] = \
                            canvas_height - (shape_ending_list[index_y] + agent.target_position.get_y())

                    canvas.create_polygon(shape_ending_list, fill="green")

                # add polygon for the start of the agent's regular path to screen
                polygon = canvas.create_polygon(shape_starting_list, fill="blue")

                # Adapt code to allow for oval creation
                # canvas.create_oval(agent.start_position.get_x() - oval_diameter / 2,
                #                       canvas_height - agent.start_position.get_y() - oval_diameter / 2,
                #                       agent.start_position.get_x() + oval_diameter / 2,
                #                       canvas_height - agent.start_position.get_y() + oval_diameter / 2,
                #                       fill="blue")

                # store visuals of objects along side that object's agent and list of positions
                visual_object = VisualObject(polygon, agent, visual_object_list_to_add[to_add_index].positions)
                visual_object_list.append(visual_object)

                # As this visual has already been added to the canvas it no longer needs to be part of to_add list
                # so it is added to the list for it's future removal after this iteration of to_add indexes is complete
                pop_indexes.append(to_add_index)

        # remove objects from to_add list that have already been added to the canvas
        for index, pop_index in enumerate(pop_indexes):
            # must subtract index as indexes change when an object is removed
            visual_object_list_to_add.pop(pop_index - index)

        # empty list to hold indexes of object removed during iteration of list
        pop_indexes = []
        
        # loop through all objects on the canvas that must be updated during this time interval
        for index in range(0, len(visual_object_list)):
            # if any objects/agents have reached their destination remove them from canvas
            # and from the list of active canvas objects
            if len(visual_object_list[index].positions) < 2:
                if not show_destination:
                    canvas.delete(visual_object_list[index].visual)
                pop_indexes.append(index)
                break

            # declare instance variables for recursive movement of visuals
            move_x = 0
            move_y = 0
            time_processed = 0
            # set the current position of the visual to be equal to the last position in the visuals position array
            current_position = visual_object_list[index].positions[-1]

            # repeat moving object until time processed has reached predefined time step. In each iteration move to the
            # objects next position as many time as possible in this time interval (or move as close to the next time
            # postion as possible)
            while time_processed < time_step:
                # if the length of positions is two then the object has reached its destination, so must do break
                if len(visual_object_list[index].positions) < 2:
                    break
                else:
                    # the place that the visualization is moving to in this iteration is it's next position
                    next_position = visual_object_list[index].positions[-2]

                    # calculate difference in time and space between this position and next position
                    position_time_difference = next_position.get_time() - current_position.get_time()
                    x_difference = next_position.get_x() - current_position.get_x()
                    y_difference = next_position.get_y() - current_position.get_y()

                    # calculate the amount of time that the object will move for in this iteration
                    time_in_position_range = min(next_position.get_time() - time_processed - time_var,
                                                 time_step - time_processed)
                    first = (time_processed == 0)
                    time_processed=time_processed + time_in_position_range

                    # if this is the first iteration of the movement loop we must check if agent has delayed start
                    # inside this time interval
                    if first:
                        if visual_object_list[index].agent.time_range.low_bound > time_var:
                            position_time_difference = position_time_difference - \
                                (time_var - visual_object_list[index].agent.time_range.low_bound)

                    # calculate how much more/less the object should move given the ratio between how much time is in
                    # this iteration of movement and between the two positions that are being moved between
                    time_ratio = time_in_position_range / position_time_difference
                    move_x = move_x + x_difference * time_ratio
                    move_y = move_y + y_difference * time_ratio

                    # if the next position is already beyond where the time will be during the next time step then
                    # we can remove this position as we will have moved to/past the next position
                    if next_position.get_time() < time_var + time_step:
                        visual_object_list[index].positions.pop()

                    current_position = next_position

            # move visualization on canvas
            canvas.move(visual_object_list[index].visual, move_x,  - move_y)

        # remove objects from visuals list that have reached their destination
        for index, pop_index in enumerate(pop_indexes):
            # must subtract index as indexes change when an object is removed
            visual_object_list.pop(pop_index - index)

        # update time_var to be in next time step
        time_var = time_var + time_step

        time.sleep(0.01)
        tk.update()
    else:
        time.sleep(1)
        # if finished moving through model stop running
        tk.destroy()

    tk.mainloop()
