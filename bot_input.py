
from send_DTO import Action, InputAction


phase = 0

step = 0


def bot_input(dto):
    global phase
    global step

    if phase == 0 and step == 0:
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
        phase = phase + 1
        step = 0
        return InputAction('H', [Action(x=0, y=0,), Action(x=1, y=0,)]).toJSON()
