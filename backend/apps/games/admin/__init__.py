"""Games admin package."""
from .answer_admin import AnswerAdmin
from .application_admin import ApplicationAdmin
from .character_admin import CharacterAdmin
from .fraction_admin import FactionAdmin
from .game_admin import GameAdmin
from .question_admin import QuestionAdmin
from .tag_admin import TagAdmin

__all__ = ('AnswerAdmin', 'ApplicationAdmin', 'CharacterAdmin', 'FactionAdmin', 'GameAdmin', 'QuestionAdmin', 'TagAdmin')
