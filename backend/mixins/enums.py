from django.db import models
from django.utils.translation import gettext_lazy as _


class MatrixPermissionLevel(models.IntegerChoices):
    free = 0, 'Free'
    speed1 = 1, 'Camp 1'
    speed2 = 2, 'Camp 2'
    speed3 = 3, 'Camp 3'
    speed4 = 4, 'Camp 4'
    energy1 = 5, 'Energy 1'
    energy2 = 6, 'Energy 2'
    energy3 = 7, 'Energy 3'
    energy4 = 8, 'Energy 4'
    energy5 = 9, 'Energy 5'
    energy6 = 10, 'Energy 6'
    energy7 = 11, 'Energy 7'
    energy8 = 12, 'Energy 8'
    energy9 = 13, 'Energy 9'
    energy10 = 14, 'Energy 10'
    energy11 = 15, 'Energy 11'
    energy12 = 16, 'Energy 12'

class Locale(models.TextChoices):
    # all = 'no', _('Visible to all')
    ru = 'ru', _('Russian')
    en = 'en', _('English')
    it = 'it', _('Italian')
    ro = 'ro', _('Romanian')
    hu = 'hu', _('Hungarian')
    de = 'de', _('German')
    uk = 'uk', _('Ukrainian')
    fr = 'fr', _('French')
    si = 'si', _('Slovenian')
    es = 'es', _('Spanish')
    tr = 'tr', _('Turkish')
    pt = 'pt', _('Portuguese')
    cs = 'cs', _('Czech')
