import sys, os

SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.join(SCRIPTS_DIR, '../')

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'mintur'))

os.environ['DJANGO_SETTINGS_MODULE'] = (
    sys.argv[1] if len(sys.argv) >= 2 else 'mintur.settings'
)

from apps.cuentas.models import MinturUser

for user in MinturUser.objects.all():
    user.activation_key = ''
    user.is_active = True
    user.save()
