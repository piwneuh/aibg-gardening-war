import math
from urllib.robotparser import RobotFileParser

from send_DTO import Action, InputAction

phase = 0
step = 0
graded_tiles = []
shop = 1
flag = 0
counter = 0

class Graded_Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grade = 1

def copy_tiles(tiles):
    for t in tiles:
        graded_tile = Graded_Tile(t.x, t.y)
        graded_tiles.append(graded_tile)

def get_special_tiles(tiles, enemy, source):
    special_tiles = []
    for t in tiles:
        if t.bIsSpecial:
            special_tiles.append(t)
        if tile_occupied(enemy, source.tiles, t):
            special_tiles.remove(t)           
    return special_tiles

def get_mole_target(enemy):
    for t in enemy.tiles:
        if t.bIsSpecial:
            return t
    return enemy.tiles[0]
       
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
                    t.grade = 30
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
            if t.x == st.x + 3 or t.x == st.x - 3:
                if t.y == (st.y - 3) or t.y == (st.y - 2) or t.y == (st.y - 1) or t.y == st.y or t.y == (st.y + 3) or t.y == (st.y + 2) or t.y == (st.y + 1):
                    t.grade = t.grade + 1
            if t.y == st.y + 3 or t.y == st.y - 3:
                if t.x == (st.x - 2) or t.x == (st.x - 1) or t.x == st.x or t.x == (st.x + 1) or t.x == (st.x + 2):
                    t.grade = t.grade + 1
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
    return neighbours

def find_optional_buys(amount, graded_tiles, source, enemy):
    global flag
    path_tiles = source.tiles
    chosen_tiles = []
    amount = math.floor(amount)
    maxAmount = 64 - len(source.tiles) - len(enemy.tiles)
    if amount > maxAmount:
        chosen_tiles = []
        for tile in graded_tiles:
            if not tile_occupied(enemy, source.tiles, tile):
                chosen_tiles.append(tile)
        flag = flag + 1
        return chosen_tiles

    while amount > 0:
        neighbours = get_neighbours(graded_tiles, path_tiles, enemy)
        best_neighbour = get_best_neighbour(neighbours)

        path_tiles.append(best_neighbour)
        chosen_tiles.append(best_neighbour)
        amount = amount - 1
    return chosen_tiles
    

def get_best_neighbour(neighbours):
    return(neighbours[0])


def listToAction(list):
    actions = []
    for l in list:
        actions.append(Action(x=l.x, y=l.y))
    return actions

def findSpecial(dto):
    for tile in dto.source.tiles:
        if(tile.bIsSpecial):
            return tile
    if dto.source.tiles[1] is None:
        return dto.source.tiles[0]
    return dto.source.tiles[1]

def phase_zero(dto):
    global phase
    global step
    global graded_tiles

    if step == 0:
        copy_tiles(dto.tiles)
        special_tiles = get_special_tiles(dto.tiles, dto.enemy, dto.source)
        graded_tiles = calculate_tile_grades(graded_tiles, special_tiles)
        step = step + 1
        return InputAction('C', [Action(x=0, y=0, cardid=6, amount=1), Action(x=0, y=0, cardid=0, amount=1)]).toJSON()

    if step == 1:
        step = step + 1
        return InputAction('P', [Action(cardid=6, x=dto.source.tiles[0].x, y=dto.source.tiles[0].y)]).toJSON()

    if step == 2:
        step = step + 1
        return InputAction('W', [Action(amount=1, x=dto.source.tiles[0].x, y=dto.source.tiles[0].y)]).toJSON()

    if step == 3:
        step = step + 1
        return InputAction('H', [Action(x=0, y=0)]).toJSON()

    if step == 4:
        step = step + 1
        list = find_optional_buys(1, graded_tiles, dto.source, dto.enemy)
        return InputAction('L', listToAction(list)).toJSON()

    if step == 5:
        step = step + 1
        if(findSpecial(dto).bIsSpecial):
            return InputAction('C', [Action(x=0, y=0, cardid=6, amount=1), Action(x=0, y=0, cardid=0, amount=1)]).toJSON()
        else:
            return InputAction('C', [Action(x=0, y=0, cardid=5, amount=2), Action(x=0, y=0, cardid=0, amount=10)]).toJSON()
    if step == 6:
        step = step + 1
        if(findSpecial(dto).bIsSpecial):
            return InputAction('P', [Action(cardid=6, x=findSpecial(dto).x, y=findSpecial(dto).y)]).toJSON()
        else:
            return InputAction('P', ownedTilesToAction(dto, 5)).toJSON()

    if step == 7:
        step = step + 1
        if(dto.source.tiles[1].bIsSpecial):
            return InputAction('W', [Action(amount=1, x=findSpecial(dto).x, y=findSpecial(dto).y)]).toJSON()
        else:
            return InputAction('W', watering(dto)).toJSON()

    if step == 8:
        phase = 1
        step = 0
        return InputAction('H', [Action(x=0, y=0)]).toJSON()


def getAmount(dto):
    amount = (dto.source.gold - 3000 - len(dto.source.tiles)*2000) / 7000
    return amount


def ownedTilesToAction(dto, cardid):
    actions = []
    for i in range(0, len(dto.source.tiles)):
        actions.append(Action(cardid=cardid, x=dto.source.tiles[i].x, y=dto.source.tiles[i].y))
    return actions


def watering(dto):
    actions = []
    cans = 0
    if dto.daysTillRain == 1 or dto.source.tiles[0].plantDTO.waterNeeded == 3:
        cans = 3
    else:
        cans = 5
    for i in range(0, len(dto.source.tiles)):
        actions.append(Action(amount=cans, x=dto.source.tiles[i].x, y=dto.source.tiles[i].y))
    return actions

def end_phase(dto):
    global phase
    global step
    global shop
    owned = len(dto.source.tiles)
    if step == 0 and shop == 1:
        step = step + 1
        shop = 0
        return InputAction('C', [Action(x=0, y=0, cardid=2, amount=4),
                                 Action(x=0, y=0, cardid=5, amount=owned*4),
                                 Action(x=0, y=0, cardid=0, amount=owned*20),
                                 Action(x=0, y=0, cardid=1, amount=4)]).toJSON()

    if step == 0 and shop == 0:
        step = step + 1
        target = get_mole_target(dto.enemy)
        return InputAction('M', [Action(x=target.x, y=target.y)]).toJSON()

    if step == 1 and shop == 0:
        step = step + 1
        target = get_mole_target(dto.enemy)
        return InputAction('M', [Action(x=target.x, y=target.y)]).toJSON()

    if step == 2:
        step = step + 1
        return InputAction('P', ownedTilesToAction(dto, 5)).toJSON()

    if step == 3:
        step = step + 1
        return InputAction('F', [Action(x=0, y=0)]).toJSON()

    if step == 4:
        step = step + 1
        return InputAction('W', watering(dto)).toJSON()

    if step == 5:
        step = 0
        if(dto.source.cards[5].owned == 0):
            shop = 1
        return InputAction('H', [Action(x=0, y=0)]).toJSON()

def def_phase(dto):
    global phase
    global step
    global shop
    global counter
    
    owned = len(dto.source.tiles)
    if step == 0 and shop == 1:
        step = step + 1
        shop = 0
        return InputAction('C', [Action(x=0, y=0, cardid=2, amount=4),
                                 Action(x=0, y=0, cardid=5, amount=owned*4),
                                 Action(x=0, y=0, cardid=0, amount=owned*20),
                                 Action(x=0, y=0, cardid=1, amount=4)]).toJSON()

    if step == 0 and shop == 0:
        step = step + 1
        target = get_mole_target(dto.enemy)
        return InputAction('M', [Action(x=target.x, y=target.y)]).toJSON()

    if step == 1 and shop == 0:
        step = step + 1
        target = get_mole_target(dto.enemy)
        return InputAction('M', [Action(x=target.x, y=target.y)]).toJSON()
    
    if step == 2 and shop == 0:
        step = step + 1
        target = get_mole_target(dto.enemy)
        return InputAction('M', [Action(x=target.x, y=target.y)]).toJSON()

    if step == 3:
        step = step + 1
        return InputAction('P', ownedTilesToAction(dto, 5)).toJSON()

    if step == 4:
        step = step + 1
        return InputAction('F', [Action(x=0, y=0)]).toJSON()

    if step == 5:
        step = step + 1
        return InputAction('W', watering(dto)).toJSON()

    if step == 6:
        step = 0
        if dto.source.cards[5].owned == 0:
            shop = 1
        return InputAction('H', [Action(x=0, y=0)]).toJSON()

def phase_one(dto):
    global phase
    global step
    global graded_tiles
    global flag

    if len(dto.source.tiles) == 1:
        phase = 0
        step = 0
        return phase_zero(dto)

    amount = getAmount(dto)

    if step == 0 and amount >= 1:
        step = step + 1
        list = find_optional_buys(getAmount(dto), graded_tiles, dto.source, dto.enemy)
        if flag == 2:
            phase = 2
            step = 0
            return end_phase(dto)
        return InputAction('L', listToAction(list)).toJSON()
    elif step == 0 and amount < 1:
        step = step + 1

    if step == 1:
        step = step + 1
        owned = len(dto.source.tiles)
        return InputAction('C', [Action(x=0, y=0, cardid=2, amount=1),
                                 Action(x=0, y=0, cardid=5, amount=owned),
                                 Action(x=0, y=0, cardid=0, amount=owned*5)]).toJSON()

    if step == 2:
        step = step + 1
        return InputAction('P', ownedTilesToAction(dto, 5)).toJSON()

    if step == 3:
        step = step + 1
        return InputAction('F', [Action(x=0, y=0)]).toJSON()

    if step == 4:
        step = step + 1
        return InputAction('W', watering(dto)).toJSON()

    if step == 5:
        step = 0
        return InputAction('H', [Action(x=0, y=0)]).toJSON()


    return {}

def bot_input(dto):
    global phase
    global step
    global role 

    if dto.source.tiles[0].x == 0:
        role = 'ATK'
    else:
        role = 'DEF'

    if phase == 0:
        return phase_zero(dto)
    elif phase == 1:
        return phase_one(dto)
    else:
        if role == 'ATK':
            return end_phase(dto)
        else:
            return def_phase(dto)

