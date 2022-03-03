from send_DTO import Action, InputAction


def bot_input(dto):
    
    return InputAction('C', [Action(x = 0, y = 0, cardid = 6, amount = 1), Action(x = 0, y = 0, cardid = 0, amount = 1)]).toJSON()
    