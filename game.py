#!/usr/bin/env python

import random


class ScrabbleError(Exception):
    pass


class ScrabbleGame:
    # Triple word score board positions.
    triple_ws = [
        (0, 0),
        (0, 7),
        (0, 14),
        (7, 0),
        (7, 14),
        (14, 0),
        (14, 7),
        (14, 14),
    ]

    # Double word score positions.
    double_ws = [(x, x) for x in range(14)]
    double_ws.extend([(14 - x, x) for x in range(14)])

    def __init__(self, dictionary):
        self.dictionary = dictionary

        # Generate an empty Scrabble board.
        self.board = []
        for i in range(15):
            self.board.append([None] * 15)

        self.players = {}
        self.current_player = None

        # Populate tiles.
        self.tile_bag = []
        # 1 point
        self.tile_bag.extend(['E'] * 12)
        self.tile_bag.extend(['A', 'I'])
        self.tile_bag.extend(['O'] * 8)
        self.tile_bag.extend(['N', 'R', 'T'] * 6)
        self.tile_bag.extend(['L', 'S', 'U'] * 4)
        # 2 points
        self.tile_bag.extend(['D'] * 4)
        self.tile_bag.extend(['G'] * 3)
        # 3 points
        self.tile_bag.extend(['B', 'C', 'M', 'P'] * 2)
        # 4 points
        self.tile_bag.extend(['F', 'H', 'V', 'W', 'Y'] * 2)
        # 5 points
        self.tile_bag.extend(['K'])
        # 8 points
        self.tile_bag.extend(['J', 'X'])
        # 10 points
        self.tile_bag.extend(['Q', 'Z'])

        # Shuffle tile bag
        random.shuffle(self.tile_bag)

    def __str__(self):
        result = []
        result.append('Player scores:')
        for player_id, details in self.players.items():
            result.append(f"\t{details['display_name']}: {details['score']}")
        result.append('')

        repr_board = []

        for y in range(len(self.board)):
            row = self.board[y]
            for x in range(len(self.board)):
                if not self.board[y][x]:
                    if (x, y) in self.triple_ws:
                        row[x] = '3'
                    elif (x, y) in self.double_ws:
                        row[x] = '2'
                    else:
                        row[x] = '□'

            repr_board.append(row)

        for row in repr_board:
            result.append(' '.join(row))

        return '\n'.join(result)

    def add_player(self, name, identifier):
        """
        Adds a new player the the game. The identifier is a unique ID to subsequently identify the player.
        """
        if identifier in self.players:
            raise ValueError('Player already present.')

        self.players[identifier] = {
            'display_name': name,
            'score': 0,
            'tiles': random.sample(self.tile_bag, 7),
        }

    def validate_board(self):
        """
        Returns True if the board is in a valid state. False or raise an Exception otherwise.
        """
        def find_connected_tiles(x, y, visited=[]):
            """
            Returns a list of all (x, y) positions which are connected horizontally or vertically
            to the center tile.
            """
            if (x, y) not in visited:
                neighbors = []
                if x > 0 and self.board[x - 1][y]:
                    neighbors.append((x - 1, y))
                if x < 15 and self.board[x + 1][y]:
                    neighbors.append((x + 1, y))
                if y > 0 and self.board[x][y - 1]:
                    neighbors.append((x, y - 1))
                if y < 15 and self.board[x][y + 1]:
                    neighbors.append((x, y + 1))

                visited.append((x, y))

                for n in neighbors:
                    find_connected_tiles(n[0], n[1], visited)

            return visited

        def translate_board(nodes):
            """
            Translates the (x, y) list returned from find_connected_tiles back into a two dimensional
            list for easy comparison with other boards.
            """
            result = []
            for i in range(15):
                result.append([None] * 15)

            for node in nodes:
                result[node[0]][node[1]] = self.board[node[0]][node[1]]

            return result

        # Do we have a center tile?
        if not self.board[7][7]:
            return False 

        connected_tiles = find_connected_tiles(7, 7)
        # Is the center tile all alone?
        if len(connected_tiles) == 1:
            return False

        connected_board = translate_board(connected_tiles)
        if connected_board != self.board:
            return False

        return True

    def select_first_player(self):
        """
        Randomly pick a player to start the game. Returns their player ID.
        """
        self.current_player = random.choice(list(self.players.keys()))

        return self.current_player

    def select_next_player(self):
        """
        Selects and returns the player ID of the player whose turn is next.
        """
        player_ids = list(self.players.keys())

        self.current_player = player_ids[(player_ids.index(self.current_player) + 1) % len(player_ids)]

        return self.current_player

    def get_current_player(self):
        """
        Returns the player ID of the player whose turn it currently is.
        """
        return self.current_player

    def take_turn(self, word, position, direction):
        """
        Takes a new turn, inserting the word `word` into the (x, y) `position` and following
        the direction down `D` or right `R`.
        """
        if direction != 'D' and direction != 'R':
            raise ScrabbleError('Invalid direction specified.')

        # Use the find_words method to retrieve a list of all valid words for the players tiles.
        valid_words = self.dictionary.find_words(self.players[self.current_player]['tiles'])

        if not word in valid_words:
            raise ScrabbleError('Invalid word from your tileset.')

        y_mod = 1 if direction == 'D' else 0
        x_mod = 1 if direction == 'R' else 0

        score_diff = 0

        #                 *1  *2  *3
        ws_mulitpliers = [1,  1,  1]  # Multiply score by element.
        # Verify that the player can place the word.
        for i in range(len(word)):
            current_cell = self.board[position[1] + i * y_mod][position[0] + i * x_mod]

            if current_cell and not current_cell == word[i]:
                raise ScrabbleError('Tile overlap not allowed.')

        # Duplicate the board to make temporary modifications to.
        board = [row[:] for row in self.board]
        for i in range(len(word)):
            board[position[1] + i * y_mod][position[0] + i * x_mod] = word[i]

            # Check if we intersect with a double or triple word score cell.
            if position in self.triple_ws:
                ws_mulitpliers[2] += 1
            elif position in self.double_ws:
                ws_mulitpliers[1] += 1

            # Add to score.
            if word[i] in ['Q', 'Z']:
                score_diff += 10
            elif word[i] in ['J', 'X']:
                score_diff += 8
            elif word[i] in ['K']:
                score_diff += 5
            elif word[i] in ['F', 'H', 'V', 'W', 'Y']:
                score_diff += 4
            elif word[i] in ['B', 'C', 'M', 'P']:
                score_diff += 3
            elif word[i] in ['D', 'G']:
                score_diff += 2
            else:
                score_diff += 1

            # ToDo: Permit gaps in a players chosen word.

        for multiplier in ws_mulitpliers:
            score_diff *= multiplier

        # Verify that the new board layout is valid.
        curr_board = self.board
        self.board = board
        if not self.validate_board():
            self.board = curr_board
            raise ScrabbleError('Invalid move.')

        self.players[self.current_player]['score'] += score_diff
        self.players[self.current_player]['tiles'].extend(random.sample(self.tile_bag,
            min(7, len(self.tile_bag))))

        # We're done here.
        self.select_next_player()

        return score_diff, self.get_current_player()
