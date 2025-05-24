from django.utils.translation import gettext_lazy as _

SL_BEGINNER = 'beginner'
SL_INTERMEDIATE = 'intermediate'
SL_ADVANCED = 'advanced'
SL_EXPERT = 'expert'

SKILL_LEVELS = [
    (SL_BEGINNER, _('Beginner')),
    (SL_INTERMEDIATE, _('Intermediate')),
    (SL_ADVANCED, _('Advanced')),
    (SL_EXPERT, _('Expert')),
]

CT_EMAIL = 'email'
CT_PHONE = 'phone'
CT_LINKEDIN = 'linkedin'
CT_GITHUB = 'github'
CT_WEBSITE = 'website'
CT_TELEGRAM = 'telegram'
CT_SKYPE = 'skype'
CT_OTHER = 'other'

CONTACT_TYPES = [
    (CT_EMAIL, 'Email'),
    (CT_PHONE, 'Phone'),
    (CT_LINKEDIN, 'LinkedIn'),
    (CT_GITHUB, 'GitHub'),
    (CT_WEBSITE, 'Website'),
    (CT_TELEGRAM, 'Telegram'),
    (CT_SKYPE, 'Skype'),
    (CT_OTHER, 'Other'),
]


# Language mappings for different services
SUPPORTED_LANGUAGES = {
    'kw': {
        'name': 'Cornish',
        'google': 'co',
    },  # Cornish not widely supported
    'gv': {
        'name': 'Manx',
        'google': None,
    },  # Very rare language
    'br': {
        'name': 'Breton',
        'google': 'br',
    },
    'iu': {
        'name': 'Inuktitut',
        'google': None,
    },
    'kl': {
        'name': 'Kalaallisut',
        'google': None,
    },
    'rom': {
        'name': 'Romani',
        'google': None,
    },
    'oc': {
        'name': 'Occitan',
        'google': 'oc',
    },
    'lad': {
        'name': 'Ladino',
        'google': None,
    },
    'se': {
        'name': 'Northern Sami',
        'google': None,
    },
    'hsb': {
        'name': 'Upper Sorbian',
        'google': None,
    },
    'csb': {
        'name': 'Kashubian',
        'google': None,
    },
    'zza': {
        'name': 'Zazaki',
        'google': None,
    },
    'cv': {
        'name': 'Chuvash',
        'google': None,
    },
    'liv': {
        'name': 'Livonian',
        'google': None,
    },
    'tsd': {
        'name': 'Tsakonian',
        'google': None,
    },
    'srn': {
        'name': 'Saramaccan',
        'google': None,
    },
    'bi': {
        'name': 'Bislama',
        'google': None,
    },
}
