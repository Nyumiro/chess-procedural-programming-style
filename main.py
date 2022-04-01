import copy
from functions import *

desk = initDesk()
history = {0: copy.deepcopy(desk)}

step_counter = 0
isWhitePlayer = True
print('\nПоддержка рокировки и сложных правил для пешки не реализована.')
print('Для отката ходов используйте команду revert-n, где n - на сколько ходов откатиться.')
printDesk(desk)
while True:
    step_counter += 1

    print(f'Ход №{step_counter}.')
    print(f"Ходят {'белые' if isWhitePlayer else 'черные'}. ")

    inp = input('Введите ход (пример: a7-a6): ')

    if 'revert' in inp:
        step_number = int(inp.split('-')[-1])
        step_counter = step_counter - step_number if (step_counter - step_number) > 0 else 0
        isWhitePlayer = step_counter % 2 != 0
        desk = history[step_counter]
        printDesk(desk)
        print(f'Игра откатилась к началу.' if step_counter == 0 else 'Игра откатилась к {step_counter+1} ходу.')
        continue

    step = tryParseInput(inp, desk)
    if not step:
        continue

    position_start, position_end = step

    figure = desk[position_start]

    if isWhitePlayer ^ figure.isupper():
        print('Вы не можете ходить фигурами оппонента. Повторите ввод.')
        continue

    if not checkStep(figure, position_start, position_end, desk):
        print(f'Недопустимая траектория для фигуры {figure}. Повторите ввод.')
        continue

    if figure not in 'Nn' and hasObstacle(position_start, position_end, desk):
        continue

    if position_end in desk:
        if isWhitePlayer ^ desk[position_end].islower():
            print(f'Поле {position_end} занято союзной фигурой.')
            continue
        print(f'Съедена фигура {desk[position_end]}.')
    desk[position_end] = figure
    del desk[position_start]
    printDesk(desk)
    if check(desk, not isWhitePlayer):
        if checkMate(desk, not isWhitePlayer):
            print(f"Мат королю {'белых' if not isWhitePlayer else 'черных'}. "
                  f"Победа {'белых' if isWhitePlayer else 'черных'}. "
                  f"Игра окончена за количество ходов: {step_counter}.")
            break
        print(f"Король {'белых' if not isWhitePlayer else 'черных'} под шахом.")
    history[step_counter] = copy.deepcopy(desk)
    isWhitePlayer = not isWhitePlayer
