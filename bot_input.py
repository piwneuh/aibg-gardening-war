
from send_DTO import Action, InputAction



phase = 0

step = 0
graded_tiles = []

class Graded_Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grade = 1

def copy_tiles(tiles):
    for t in tiles:
        graded_tile = Graded_Tile(t.x, t.y)
        graded_tiles.append(graded_tile)
    
    

def bot_input(dto):

    global phase
    global step
    global graded_tiles

    if phase == 0 and step == 0:
        copy_tiles(dto.tiles)
        special_tiles = get_special_tiles(dto.tiles, dto.enemy, dto.source)
        graded_tiles = calculate_tile_grades(graded_tiles, special_tiles)
        print(graded_tiles[5].grade)
        print(graded_tiles[2].grade)

        
        step = step + 1
        return InputAction('C', [Action(x=0, y=0, cardid=6, amount=1), Action(x=0, y=0, cardid=0, amount=1)]).toJSON()

    if phase == 0 and step == 1:
        step = step + 1
        return InputAction('P', [Action(cardid=6, x=0, y=0,)]).toJSON()

    if phase == 0 and step == 2:
        step = step + 1
        return InputAction('W', [Action(amount=1, x=0, y=0,)]).toJSON()

    if phase == 0 and step == 3:
        phase = phase + 1
        step = 0
        return InputAction('H', [Action(x=0, y=0,)]).toJSON()


    if phase == 1 and step == 0:

        step = step + 1
        return InputAction('L', [Action(x=1, y=0)]).toJSON()


    if phase == 1 and step == 1:
        step = step + 1
        return InputAction('C', [Action(x=0, y=0, cardid=5, amount=2), Action(x=0, y=0, cardid=0, amount=10)]).toJSON()

    if phase == 1 and step == 2:
        step = step + 1
        return InputAction('P', [Action(cardid=5, x=0, y=0,), Action(cardid=5, x=1, y=0,)]).toJSON()

    if phase == 1 and step == 3:
        step = step + 1
        return InputAction('W', [Action(amount=5, x=0, y=0,), Action(amount=5, x=1, y=0,)]).toJSON()

    if phase == 1 and step == 4:
        list = find_optional_buys(6, graded_tiles, dto.source, dto.enemy)
        for l in list:
            print("DA KUPI SLEDECE:", l.x, l.y)


        phase = phase + 1
        step = 0
        return InputAction('H', [Action(x=0, y=0,), Action(x=1, y=0,)]).toJSON()

def get_special_tiles(tiles, enemy, source):
    special_tiles = []
    for t in tiles:
        if t.bIsSpecial:
            special_tiles.append(t)
        if tile_occupied(enemy, source.tiles, t):
            special_tiles.remove(t)           
    return special_tiles
       
def tile_occupied(enemy, source_tiles, tile):
    for t in enemy.tiles:
        if t == tile:
            return True
    for t in source_tiles:
        if t == tile:
            return True
    return False

def calculate_tile_grades(tiles, special_tiles):
    for st in special_tiles:
        for t in tiles:
            if t.x == st.x:
                if t.y == st.y:
                    t.grade = 20
                if t.y == (st.y - 1) or t.y == (st.y + 1) :
                    t.grade = t.grade + 3
            if t.x == st.x + 1 or t.x == st.x - 1:
                if t.y == (st.y - 1) or t.y == (st.y + 1) or t.y == st.y:
                    t.grade = t.grade + 3
            if t.x == st.x + 2 or t.x == st.x - 2:
                if t.y == (st.y - 2) or t.y == (st.y - 1) or t.y == st.y or t.y == (st.y + 2) or t.y == (st.y + 1):
                    t.grade = t.grade + 2
            if t.y == st.y + 2 or t.y == st.y - 2:
                if t.x == (st.x - 1) or t.x == st.x or t.x == (st.x + 1):
                    t.grade = t.grade + 2
    return tiles

def get_neighbours(tiles, path_tiles, enemy):
    neighbours = []
    for st in path_tiles:
        for t in tiles:
            if t.x == st.x:
                if (t.y == st.y - 1 or t.y == st.y + 1) and not tile_occupied(enemy, path_tiles, t):  
                    neighbours.append(t)
            if t.x == st.x + 1 or t.x == st.x - 1:
                if (t.y == st.y - 1 or t.y == st.y + 1 or t.y == st.y) and not tile_occupied(enemy, path_tiles, t):  
                    neighbours.append(t)
    neighbours.sort(key=lambda x: x.grade, reverse=True)
    print(neighbours)
    return neighbours

def find_optional_buys(amount, graded_tiles, source, enemy):
    path_tiles = source.tiles
    chosen_tiles = []
    while amount > 0:
        neighbours = get_neighbours(graded_tiles, path_tiles, enemy)
        best_neighbour = get_best_neighbour(neighbours)

        path_tiles.append(best_neighbour)
        chosen_tiles.append(best_neighbour)
        amount = amount - 1
    return chosen_tiles
    

def get_best_neighbour(neighbours):
    print(neighbours[1].x, neighbours[1].y)
    return(neighbours[1])               
            



