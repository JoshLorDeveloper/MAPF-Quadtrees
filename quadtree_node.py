from agent import Agent
from range import Range


class QuadTreeNode:

    THRESHOLD = 5

    def __init__(self, range_x: Range, range_y: Range, time_range: Range, root=False):
        self.children = []
        self.agents = []
        self.range_x = range_x
        self.range_y = range_y
        self.time_range = time_range
        self.root = root

    def add_agent(self, agent: Agent):
        # if has children add to children otherwise add to self
        if len(self.children) > 0:
            self.add_agent_to_children(agent)

        # check if agent should not be added to quadtree node.
        if self.condition_to_not_add(agent):
            return

        # add agent to agent list
        self.agents.append(agent)

        # if after adding agent quadtree contains too many agents it must split
        if len(self.agents) > self.THRESHOLD:
            self.split()

    def add_agents(self, agents_to_add: [Agent]):
        # if has children add to children otherwise add to self
        if len(self.children) > 0:
            self.add_agents_to_children(agents_to_add)

        # remove agents that should not be added from list of agents to be added
        agents_to_add = [agent for agent in agents_to_add if not self.condition_to_not_add(agent)]

        if len(agents_to_add) == 0:
            return

        # add agents to agents list
        self.agents.extend(agents_to_add)

        # if after adding agents quadtree contains too many agents it must split
        if len(self.agents) > self.THRESHOLD:
            self.split()

    def condition_to_not_add(self, agent: Agent):
        # ensure that agent in quadtree 3d spacial area and that quadtree does not already contain agent
        return agent in self.agents or not self.contains_agent(agent)

    def add_agent_to_children(self, agent: Agent):
        for child in self.children:
            child.add_agent(agent)

    def add_agents_to_children(self, agents: [Agent]):
        for child in self.children:
            child.add_agents(agents)

    # NOTE IN CURRENT IMPLEMENTATION CONTAINS AGENT WILL NEVER RETURN FALSE BECAUSE OF TIME WHICH MEANS THAT IT IS A
    # WASTED O(logn operation).
    # ALTHOUGH BE AWARE THAT IF THIS IS REMOVED QUADTREE PARENTS WILL NO LONGER BE ADDED TO PositionIndexedDictionary
    def contains_agent(self, agent: Agent):
        # if increased efficiency is needed can be adapted to not check if time range is correct, although will cause
        # problems with quadtree parents not being added
        if agent.is_in(self):
            return True
        return False

    def split(self):
        # split 2d area into four equal 2d spaces
        for index in range(1, 5):
            self.children.append(QuadTreeNode(self.range_x.split(2 - index % 2),
                                              self.range_y.split(2 - ((index + 1) // 2) % 2),
                                              self.time_range))

        # remove quadtree parents from quadtree nodes children, as this quadtree node is no longer the direct parent
        # it is rather this quadtree nodes child that will be the direct parent
        for agent in self.agents:
            agent.remove_quadtree_parent(self, self.time_range)

        # add these agents to quadtree nodes children
        self.add_agents_to_children(self.agents)
