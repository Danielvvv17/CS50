import random


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
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

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

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1: Mark the cell as a move made
        self.moves_made.add(cell)

        # Step 2: Mark the cell as safe
        self.mark_safe(cell)

        # Step 3: Add a new sentence to the knowledge base
        neighbors = set()
        i, j = cell
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di, dj) == (0, 0):
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    if (ni, nj) not in self.safes:
                        if (ni, nj) in self.mines:
                            count -= 1
                        else:
                            neighbors.add((ni, nj))

        if neighbors:
            self.knowledge.append(Sentence(neighbors, count))

        # Step 4: Mark any additional cells as safe or mines
        self.update_knowledge()

        # Step 5: Infer new sentences from existing knowledge
        self.infer_new_sentences()

    def update_knowledge(self):
        """
        Update the knowledge base by marking cells as safe or mines
        based on the current knowledge.
        """
        updated = True
        while updated:
            updated = False
            for sentence in self.knowledge:
                for mine in sentence.known_mines():
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        updated = True
                for safe in sentence.known_safes():
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        updated = True
            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

    def infer_new_sentences(self):
        """
        Infer new sentences by combining existing sentences in the knowledge base.
        """
        new_knowledge = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                    inferred_cells = sentence2.cells - sentence1.cells
                    inferred_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(inferred_cells, inferred_count)
                    if new_sentence not in self.knowledge and new_sentence not in new_knowledge:
                        new_knowledge.append(new_sentence)
        self.knowledge.extend(new_knowledge)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        choices = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        if choices:
            return random.choice(choices)
        return None
