from PIL import Image
import numpy as np
import numba
from numba import jit

@jit(nopython=True)
def get_state(field, x, y):
    if x < 0 or y < 0 or x >= field.shape[0] or y >= field.shape[1]:
        return 0
    return field[x,y]

@jit(nopython=True)
def check_dependency(x, y, old_field, dependency):
    for dep in dependency:
        locx = dep[0][0]
        locy = dep[0][1]
        if get_state(old_field, x+locx, y+locy) != dep[1]:
            return False 
    return True

@jit(nopython=True)
def step_cell(x, y, old_field, transitions):
    for transition in transitions:
        dependency = transition[0]
        new_state = transition[1]
        if check_dependency(x, y, old_field, dependency):
            return new_state
    return old_field[x, y]

@jit(nopython=True)
def step_jit(old_field, transitions):
    new_field = np.empty((old_field.shape[0], old_field.shape[1]), dtype=np.int32)
    for x in range(old_field.shape[0]):
        for y in range(old_field.shape[1]):
            cell = step_cell(x, y, old_field, transitions)
            new_field[x, y] = cell
    return new_field

class Automata():
    def __init__(self, name):
        self.name = name
        self.states = []
        self.state_color = {}
        self.state_number = {}
        self.state_pic = {}
        self.transitions = []
        self.add_state("EMPTY")

    def step(self):
        self.field = step_jit(self.field, self.transitions)

    def create_field(self, x, y):
        self.field = np.zeros((x, y), dtype=np.int32)
    
    def set_cell(self, x, y, state):
        if type(state) == str:
            self.field[x,y] = self.state_number[state]
        else:
            self.field[x,y] = state

    def render_pixel(self):
        pic = Image.new('RGB', (self.field.shape[0], self.field.shape[1]), "white")
        for x in range(self.field.shape[0]):
            for y in range(self.field.shape[1]):
                color = self.state_color[self.field[x,y]]
                pic.putpixel((x,y), (color[0], color[1], color[2]))
        return pic
    
    def print_states(self):
        for i, state in enumerate(self.states):
            print(str(i) + " " + state)

    def pixel_to_string(self, x,y):
        cell = self.field[x,y]
        color = self.state_color[cell]
        name = ""
        for state in self.states:
            if self.state_number[state] == cell:
                name = state
        
        return str(cell)+" '"+name+"' "+str(color)

    def get_state(self, x, y):
        if x < 0 or y < 0 or x >= self.field.shape[0] or y >= self.field.shape[1]:
            return 0
        return self.field[x,y]

    def add_state(self, state, color = [0,0,0]):
        self.states.append(state)
        self.state_number[state] = len(self.states)-1
        self.state_color[self.state_number[state]] = color
    

    def add_var(self, var, values):
        self.var[var] = [self.state_number[value] for value in values]

    def add_transition(self, dependency, new_state):
        for dep in dependency:
            state = dep[1]
            if type(state) == str:
                dep = (dep[0], self.state_number[state])
        if type (new_state) == str:
            new_state = self.state_number[new_state]
        self.transitions.append((dependency, new_state))



    def just_transform(self, state1, state2):
        dependency = [((0,0),state1)]
        self.add_transition(dependency=dependency, new_state=state2)

    def tranform_when_neighbour(self, state1, state2, neighbour):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                dependency = [((0,0),state1), ((i,j),neighbour)]
                self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_close_neighbour(self, state1, state2, neighbour):
        dependency = [((0,0),state1), ((0,1),neighbour)]
        self.add_transition(dependency=dependency, new_state=state2)
        dependency = [((0,0),state1), ((1,0),neighbour)] 
        self.add_transition(dependency=dependency, new_state=state2)
        dependency = [((0,0),state1), ((0,-1),neighbour)]
        self.add_transition(dependency=dependency, new_state=state2)
        dependency = [((0,0),state1), ((-1,0),neighbour)]

    def transform_when_E_W(self, state1, state2, E, W):
        dependency = [((0,0),state1), ((1,0),E), ((-1,0),W)]
        self.add_transition(dependency=dependency, new_state=state2)        
        

    def transform_when_N_S(self, state1, state2, N, S):
        dependency = [((0,0),state1), ((0,1),N), ((0,-1),S)]
        self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_N_E(self, state1, state2, N, E):
        dependency = [((0,0),state1), ((0,1),N), ((1,0),E)]
        self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_N_W(self, state1, state2, N, W):
        dependency = [((0,0),state1), ((0,1),N), ((-1,0),W)]
        self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_S_E(self, state1, state2, S, E):
        dependency = [((0,0),state1), ((0,-1),S), ((1,0),E)]
        self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_S_W(self, state1, state2, S, W):
        dependency = [((0,0),state1), ((0,-1),S), ((-1,0),W)]
        self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_N(self, state1, state2, N):
        dependency = [((0,0),state1), ((0,1),N)]
        self.add_transition(dependency=dependency, new_state=state2)
    
    def transform_when_E(self, state1, state2, E):
        dependency = [((0,0),state1), ((1,0),E)]
        self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_S(self, state1, state2, S):
        dependency =  [((0,0),state1), ((0,-1),S)]
        self.add_transition(dependency=dependency, new_state=state2)

    def transform_when_W(self, state1, state2, W):
        dependency = [((0,0),state1), ((-1,0),W)]
        self.add_transition(dependency=dependency, new_state=state2)
