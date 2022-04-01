COLUMN_NAMES = 'ABCDEFGH'


def initDesk():
    """ Данная функция заполняет словарь, представляющий игровое поле, стартовыми значениями. """
    global COLUMN_NAMES
    desk = {}
    for column in range(8):
        desk[COLUMN_NAMES[column] + '8'] = 'RNBQKBNR'[column]
        desk[COLUMN_NAMES[column] + '7'] = 'P'
        desk[COLUMN_NAMES[column] + '1'] = 'rnbqkbnr'[column]
        desk[COLUMN_NAMES[column] + '2'] = 'p'
    return desk


def figures_to_unicode(desk):
    """ Данную функцию можно использовать для вывода фигур с использованием символов юникод. """
    unicode_figures = {'K': "\u2654",
                       'Q': '\u2655',
                       'R': '\u2656',
                       'B': '\u2657',
                       'N': '\u2658',
                       'P': '\u2659',
                       'k': '\u265A',
                       'q': '\u265B',
                       'r': '\u265C',
                       'b': '\u265D',
                       'n': '\u265E',
                       'p': '\u265F'
                       }
    new_desk = {k: unicode_figures[v] for k, v in desk.items()}
    return new_desk


def printDesk(desk):
    print(' ---------------------')
    print('    A B C D E F G H\n')
    for row in range(1, 9):
        print(row, end='\t')
        for column in 'ABCDEFGH':
            position = column + str(row)
            print(desk[position] if position in desk else '.', end=' ')
        print('  ' + str(row))
    print('\n    A B C D E F G H')
    print(' ---------------------')


def isEmptyPosition(position, desk):
    if not (position in desk):
        print(f'В клетке {position} нет фигуры. Повторите ввод.')
        return True
    return False


def isIncorrectPosition(position):
    global COLUMN_NAMES
    if not len(position) == 2 or position[-1] not in '12345678' or position[0] not in COLUMN_NAMES:
        print(f'Некорректная позиция {position} для шахматной доски. Повторите ввод.')
        return True
    return False


def tryParseInput(step, desk):
    """ Данная функция обрабатывает ввод хода: производит несколько проверок корректности и вызывает ранее
    объявленные функции проверок.
    Возвращаемый объект -- кортеж вида (0; 1) == поле, из которого ходят; поле, куда ходят. """
    step = step.upper().split('-')
    if len(step) != 2:
        print('Некорректный формат хода.')
        return None
    position_start, position_end = step[0], step[1]
    if position_start == position_end:
        print('Конечная и начальная позиции совпадают. Повторите ввод.')
        return None
    if isIncorrectPosition(position_start) or isIncorrectPosition(position_end) or isEmptyPosition(position_start,
                                                                                                   desk):
        return None

    return position_start, position_end


def moveVector(start, end):
    """ Функция, возвращающая вектор перемещения фигуры. """
    global COLUMN_NAMES
    start, end = (COLUMN_NAMES.index(start[0]), int(start[-1])), (COLUMN_NAMES.index(end[0]), int(end[-1]))
    return end[0] - start[0], end[-1] - start[-1]


def sgn(number):
    """ Вспомогательная функция, определяющая знак переданного числа.
    Почему в Питоне она не является встроенной О_О... """
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def check(desk, isWhitePlayer):
    """ Функция, проверяющая наличие шаха королю оппонента. """
    king_position = \
        [k for k, v in desk.items() if isWhitePlayer and desk[k] == 'K' or not isWhitePlayer and desk[k] == 'k'][0]
    for _ in desk:
        if (isWhitePlayer ^ desk[_].isupper()) and checkStep(desk[_], _, king_position, desk):
            return True
    return False


def isCheckPosition(desk, isWhitePlayer, king_position):
    for _ in desk:
        if (isWhitePlayer ^ desk[_].isupper()) and checkStep(desk[_], _, king_position, desk):
            return True
    return False


def checkMate(desk, isWhitePlayer):  # Функция проверки мата.
    global COLUMN_NAMES
    king_position = \
        [k for k, v in desk.items() if isWhitePlayer and desk[k] == 'K' or not isWhitePlayer and desk[k] == 'k'][0]
    vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    # лист со всеми возможными векторами перемещения короля.
    for vector in vectors:
        position_int = COLUMN_NAMES.index(king_position[0]), int(king_position[-1])
        position_end_int = vector[0] + position_int[0], vector[1] + position_int[1]
        if 0 < position_end_int[0] < len(COLUMN_NAMES) and 0 < position_end_int[-1] <= 8:
            position_end = COLUMN_NAMES[position_end_int[0]] + str(position_end_int[-1])
            # получили клетку, куда король возможно может сбежать.
            if (position_end not in desk) or (desk[position_end].isupper() ^ isWhitePlayer):
                # если на конечной позиции нет союзной фигуры, которая блокирует перемещение короля, то проверим эти
                # ъпозиции
                if not isCheckPosition(desk, isWhitePlayer, king_position):
                    return False
    return True


def checkStep(figure, start, end, desk):
    """ Проверяет, может ли выбранная фигура ходить по заданной игроком траектории. """
    v = moveVector(start, end)

    if figure in 'Nn':
        return n(v)
    if figure in 'Pp':
        return p(start, end, v, figure, desk)
    if figure in 'Bb':
        return b(v)
    if figure in 'Qq':
        return q(v)
    if figure in 'Kk':
        return k(v)
    if figure in 'Rr':
        return r(v)
    return True


def hasObstacle(start, end, desk):
    """ Функция проверяет наличие препятствий по ходу фигуры. """
    global COLUMN_NAMES
    v = moveVector(start, end)
    position_start_int = COLUMN_NAMES.index(start[0]), int(start[-1])
    for i in range(1, max(abs(v[0]), abs(v[1]))):
        column = COLUMN_NAMES[position_start_int[0] + i * sgn(v[0])]
        row = position_start_int[1] + i * sgn(v[1])
        position = column + str(row)
        if position in desk:
            print(f'В поле {position} стоит {desk[position]}. Повторите ход.')
            return True
    return False


# .............................................................

""" Ниже объявлены функции, проверяющие корректность вектора хода всех шахматных фигур. """


def p(s, e, v, f, d):  # старт, энд, вектор, фигура, доска
    """ Пешка. """
    if f.islower() and s[-1] == '2' and v == (0, 2):
        return True
    if f.isupper() and s[-1] == '7' and v == (0, -2):
        return True

    if f.islower() and (v == (-1, 1) or v == (1, 1)) and e in d:
        return True
    if f.isupper() and (v == (1, -1) or v == (-1, -1)) and e in d:
        return True

    if f.islower() and v == (0, 1):
        return True
    if f.isupper() and v == (0, -1):
        return True
    return False


def n(v):
    """ Конь. """
    return (abs(v[0]), abs(v[-1])) == (2, 1) or (abs(v[0]), abs(v[-1])) == (1, 2)


def b(v):
    """ Слон. """
    return abs(v[0]) == abs(v[1])


def q(v):
    """ Королева. """
    return (abs(v[0]) == abs(v[1])) or v[0] == 0 or v[1] == 0


def r(v):
    """ Ладья. """
    return v[0] == 0 or v[1] == 0


def k(v):
    """ Король. """
    return abs(v[0]) <= 1 and abs(v[1]) <= 1
