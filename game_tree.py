import copy

MOVEMENT_VECTORS = [
    (-1, -1), (-1, 0), (-1, 1),
    (1, -1), (1, 0), (1, 1),
    (0, -1), (0, 1)
]


class PositionNode:
    def __init__(self, position: list[list[str]], to_move='1'):
        self.position: list[list[str]] = position
        self.to_move = to_move
        self.children: list[PositionNode] = []
        self.children_positions = []
        self.rating = None

    def root_initialization(self, max_depth: int, depth=0):
        if depth == max_depth:
            return
        if not self.children:
            self.find_children()
        for child in self.children:
            child.root_initialization(max_depth, depth+1)
        return

    def find_children(self) -> None:
        for x in range(16):
            for y in range(16):
                if self.position[x][y] == self.to_move:
                    for dx, dy in MOVEMENT_VECTORS:
                        try:
                            if self.position[x + dx][y + dy] == '0' and x + dx >= 0 and y + dy >= 0:
                                new_position = copy.deepcopy(self.position)
                                new_position[x + dx][y + dy] = self.to_move
                                new_position[x][y] = '0'
                                self.children.append(PositionNode(new_position, '1' if self.to_move == '2' else '2'))
                                self.children_positions.append(new_position)
                        except IndexError:
                            pass
                    self.find_jump_move(x, y, self.position)

    def find_jump_move(self, x: int, y: int, position):
        for dx, dy in MOVEMENT_VECTORS:
            try:
                if self.position[x + dx][y + dy] != '0' and self.position[x + 2*dx][y + 2*dy] == '0' \
                        and x + 2*dx >= 0 and y + 2*dy >= 0:
                    new_position = copy.deepcopy(position)
                    new_position[x + 2*dx][y + 2*dy] = self.to_move
                    new_position[x][y] = '0'
                    if new_position not in self.children_positions:
                        self.children.append(PositionNode(new_position, '1' if self.to_move == '2' else '2'))
                        self.children_positions.append(new_position)
                        self.find_jump_move(x + 2*dx, y + 2*dy, new_position)
            except IndexError:
                pass

    def winner(self) -> str:
        count_1 = 0
        count_2 = 0
        for i in range(5):
            for j in range(5):
                if i + j <= 5:
                    if self.position[i][j] == '1':
                        count_1 += 1
                    if self.position[15-i][15-j] == '2':
                        count_2 += 1
        if count_1 == 19:
            return '1'
        if count_2 == 19:
            return '2'
        return '0'

    def find_child_with_rating(self, rating: int):
        for child in self.children:
            if child.rating == rating:
                return child

    def __str__(self) -> str:
        result = ''
        for row in self.position:
            result += '\n'
            result += '|'
            for x in row:
                result += x if x != '0' else '_'
                result += '|'
        return result
