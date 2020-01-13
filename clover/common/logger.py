
import inspect

from clover.exts import db
from clover.common.models import LoggerModel


_level = ['debug', 'info', 'warning', 'error']


def log(run, case, suite, msg='', level='info', step=None):
    step = step if step else inspect.stack()[1][3]
    level = level if level in _level else 'info'
    data = {
        'run_id': run,
        'case_id': case,
        'suite_id': suite,
        'step': step,
        'level': level,
        'message': msg
    }
    model = LoggerModel(**data)
    db.session.add(model)
    db.session.commit()
