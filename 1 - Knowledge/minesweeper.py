from copy import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`

        # create a list of neighboring cells
        (cell_row, cell_column) = cell
        neighboring_cells = []
        neighboring_row = cell_row - 1
        while neighboring_row < cell_row + 2:
            if neighboring_row > self.height - 1:
                break
            neighboring_column = cell_column - 1
            while neighboring_column < cell_column + 2:
                if neighboring_row == cell_row and neighboring_column == cell_column:
                    neighboring_column += 1
                    continue
                elif neighboring_row < 0:
                    neighboring_row += 1
                    continue
                elif neighboring_column < 0:
                    neighboring_column += 1
                    continue
                elif neighboring_column > self.width - 1:
                    break
                else:
                    neighboring_cells.append((neighboring_row, neighboring_column))
                neighboring_column += 1
            neighboring_row += 1
        
        # create sentence
        new_sentence = Sentence(neighboring_cells, count)

        # check if there are mines or safes in the sentence
        # and update knowledge base
        mines_in_sentence = new_sentence.known_mines()
        safes_in_sentence = new_sentence.known_safes()
        if mines_in_sentence:
            for mine in mines_in_sentence:
                self.mark_mine(mine)
        if safes_in_sentence:
            for safe in safes_in_sentence:
                self.mark_safe(safe)

        # exclude known cells from sentence
        for item in self.safes:
            if item in new_sentence.cells:
                new_sentence.mark_safe(item)
        for item in self.mines:
            if item in new_sentence.cells:
                new_sentence.mark_mine(item)
        for item in self.moves_made:
            if item in new_sentence.cells:
                new_sentence.mark_safe(item)
        
        # if unknown cells remains, add sentence to knowledge base
        if len(new_sentence.cells) > 0:
            self.knowledge.append(new_sentence)

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:
            if sentence.count == 0:
                safes = []
                for item in sentence.cells:
                    safes.append(item)
                for item in safes:
                    self.mark_safe(item)
            elif sentence.count == len(sentence.cells):
                mines = []
                for item in sentence.cells:
                    mines.append(item)
                for mine in mines:
                    self.mark_mine(mine)

        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge
        inferred_sentences = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 == sentence2:
                    continue
                else:
                    if len(sentence1.cells) == 0 or len(sentence2.cells) == 0:
                        continue
                    difference = sentence1.cells - sentence2.cells
                    if difference:
                        continue
                    else:
                        inferred_sentences.append(Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count))
        
        for sentence in inferred_sentences:
            self.knowledge.append(sentence)

        inferred_sentences.clear()

        # check mines and safes after inferring new sentences
        mine_cells = []
        safe_cells = []
        for sentence in self.knowledge:
            if sentence.count == 0:
                for item in sentence.cells:
                    safe_cells.append(item)
            elif sentence.count == sentence.known_mines:
                for item in sentence.cells:
                    safe_cells.append(item)
        
        for item in mine_cells:
            self.mark_mine(item)
        for item in safe_cells:
            self.mark_safe(item)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # look for a safe cell not already played
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        
        # if all safe cells are played...
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # listing all cells in the board
        possible_cells = []
        for i in range(self.height):
            for j in range(self.width):
                possible_cells.append((i, j))
        
        # excluding moves made
        for cell in self.moves_made:
            if cell in possible_cells:
                possible_cells.remove(cell)        

        # excluding mines
        for cell in self.mines:
            if cell in possible_cells:
                possible_cells.remove(cell)

        # return random cell, or None
        if len(possible_cells) > 1:
            return possible_cells[random.randint(0, len(possible_cells) - 1)]
        elif len(possible_cells) == 1:
            return possible_cells
        else:
            return None
