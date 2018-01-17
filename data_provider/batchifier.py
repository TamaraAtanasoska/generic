import copy
from enum import Enum


class BatchifierSplitMode(Enum):
    NoSplit = 0
    SingleQuestion = 1
    DialogueHistory = 2


def batchifier_split_helper(games, split_mode):

    new_games = []

    # One sample = One full dialogue
    if split_mode == BatchifierSplitMode.NoSplit:
        new_games = games

    # One sample = One question
    elif split_mode == BatchifierSplitMode.SingleQuestion:
        for game in games:
            for i, q, a in zip(game.question_ids, game.questions, game.answers):
                new_game = copy.copy(game)
                new_game.questions = [q]
                new_game.question_ids = [i]
                new_game.answers = [a]

                new_games.append(new_game)

    # One sample = Subset of questions
    elif split_mode == BatchifierSplitMode.DialogueHistory:
        for game in games:
            for i in range(len(game.question_ids)):
                new_game = copy.copy(game)
                new_game.questions = game.questions[:i + 1]
                new_game.question_ids = game.question_ids[:i + 1]
                new_game.answers = game.answers[:i + 1]

                new_games.append(new_game)

    return new_games


class AbstractBatchifier(object):

    def split(self, games):
        return games

    def filter(self, games):
        return games

    def apply(self, games):
        return games
