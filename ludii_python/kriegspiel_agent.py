"""
This code is a short example demonstrating the usage of Kriegspiel-specific Ludii functions
For more information regarding Ludii AI development, please refer to the following: 
     * https://www.ludii.games/index.php
     * https://ludiitutorials.readthedocs.io/en/latest/basic_ai_api.html
     * https://ludiitutorials.readthedocs.io/en/latest/ludii_terminology.html
     * https://ludiitutorials.readthedocs.io/en/latest/cheat_sheet.html
     * https://github.com/Ludeme/LudiiPythonAI

@author Nikola Novarlic
"""

import random


class KriegspielAgent:

    def __init__(self):
        """
        Constructor
        """

        """ Our player index """
        self.player = -1

        """ Opponent player index """
        self.opponent = -1

        """ Number of players """
        self._players = 2


    def init_ai(self, game, player_id):
        """
        Initialises the AI

        :param game:
        :param player_id:
        """
        self.player = player_id
        self.opponent = self._players - player_id + 1


    def ai_player_white(self):
        """
        The function returns True if the Agent plays with white pieces
        """
        return self.player == 1


    def choose_random_move(self, pseudo_legal_moves):
        r = random.randint(0, pseudo_legal_moves.size() - 1)
        return pseudo_legal_moves.get(r)


    def select_action(self,
                      game,
                      context,
                      max_seconds,
                      max_iterations,
                      max_depth):
        """
        Returns an action to play

        :param game:
        :param context:
        :param max_seconds:
        :param max_iterations:
        :param max_depth:
        :return:
        """

        """
        * A function that returns a set of pseudo-legal moves
        * As a player, the agent has to try a move selected among the given set
        * The referee, who knows the list of legal moves for both sides, answers whether the move was legal or not
        """
        pseudo_legal_moves = game.moves(context).moves()

        """
        * Messages received from the referee after the last try
        * It contains messages announcing the position of all captures, checks, and check directions,
          or simply no messages if the move is legal without checks and captures
        * Otherwise, if the selected try is impossible to play, the only message announced is "Illegal move" 
        """
        last_try_messages = context.getNotes(self.player)
        
        if last_try_messages.size() != 0:
            if last_try_messages.get(0) == "Illegal move":
                """
                * The previously selected try is illegal on the referee's board
                * The Agent is asked for another try
                * For the simplicity terms, we would again try a random move
                """
                return self.choose_random_move(pseudo_legal_moves)

        if pseudo_legal_moves.get(0).actionDescriptionStringShort() == "Promote":
            """
            * A situation in which the agent's pawn needs to be promoted after the last move
            * In this case, pseudo_legal_moves would contain only promotion moves with different pieces
            * Use pseudo_legal_move.what() to select a move containing the desired promotion piece
            * We will play a random promotion move
            """
            return self.choose_random_move(pseudo_legal_moves)

        """
        The opponent score represents the number of pawn captures
        available to the opponent after our last legal move
        """
        opp_tries = context.score(self.opponent)

        """
        * Referee messages that are announced after the opponent's legal move
        * If the capture happened in the last turn, one of the messages would 
          specify where the capture took place and whether the captured piece is the pawn or another piece
        * If the agent's King is in check, one message would reveal the check type (rank, file, long/short diagonal, or knight) 
        """
        referee_messages = context.getNotes(self.opponent)

        """
        The player score denotes the number of legal capturing moves using pawns 
        for the current turn
        """
        pawn_tries = context.score(self.player)

        """
        * After receiving all the available information, the agent is asked to provide the next try
        * The next try needs to be selected among the set of pseudo-legal moves based on the agent's strategy
        * The Move class provides `from()` and `to()` functions that can be useful in searching pseudo-legal 
          moves for the index of the desired move
        """
        return self.choose_random_move(pseudo_legal_moves)