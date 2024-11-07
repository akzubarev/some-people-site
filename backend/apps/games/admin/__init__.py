"""Games admin package."""
from .answer import AnswerAdmin
from .application import ApplicationAdmin
from .character import CharacterAdmin
from .group import GroupAdmin
from .game import GameAdmin
from .question import QuestionAdmin
from .tag import TagAdmin

__all__ = ('AnswerAdmin', 'ApplicationAdmin', 'CharacterAdmin', 'GroupAdmin', 'GameAdmin', 'QuestionAdmin', 'TagAdmin')
