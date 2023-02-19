from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()


include(
    'components/base.py',
    'components/corsheaders.py',
    'components/database.py',
    'components/localization.py',
    'components/auth.py',
    'components/templates.py',
    'components/logging.py',
    'components/debugging.py',
)
