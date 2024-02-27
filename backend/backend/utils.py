from django.db import models
import requests
import inspect
import os
import importlib



def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_location_from_ip(ip):
    GEOLOCATION_SERVICE_URL = "http://daemon.echoip:8080/"
    ip_data = requests.get(f"{GEOLOCATION_SERVICE_URL}json?ip={ip}", verify=False).json()
    return {
        "country": ip_data.get("country", None),
        "country_iso": ip_data.get("country_iso", None),
        "city": ip_data.get("city", None),
        "longitude": ip_data.get("longitude", None),
        "latitude": ip_data.get("latitude", None),
    }

class LtreeField(models.TextField):
    description = 'ltree'

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = True
        kwargs['null'] = True
        kwargs['default'] = None
        kwargs['blank'] = True
        super(LtreeField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'ltree'


class Ancestor(models.Lookup):
    lookup_name = 'ancestor'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s @> %s' % (lhs, rhs), params


class Descendant(models.Lookup):
    lookup_name = 'descendant'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s <@ %s' % (lhs, rhs), params


LtreeField.register_lookup(Ancestor)
LtreeField.register_lookup(Descendant)


def set_types(model, name):
    modules = []
    mypath = os.path.abspath('apps')
    for module in os.listdir(mypath):
        if '.' not in module:
            path = 'apps.{}.{}'.format(module, name)
            try:
                if (importlib.util.find_spec(path)):  # importlib.util.find_loader(path)
                    modules.append(importlib.import_module(path))
            except ImportError:
                pass
    for module in modules:
        for name, obj in inspect.getmembers(module):

            if inspect.isclass(obj) and model.__name__ in name:
                setattr(model.Types, obj.__name__, obj)

def change_email(from_email, to_email, refers=[], interactive=True, strict=False):
    from apps.users.models import User
    u = User.objects.get(email__contains=from_email)
    print(f"Operation: {u.email} -> {to_email}")
    if u.email == to_email:
        print(f"Emails are same")
        return
    if len(refers):
        refers.sort()
        tmp_usr = u
        confirmations = []
        linears = [u.email]
        while tmp_usr.id != 1:
            if tmp_usr.email in refers and tmp_usr.email not in confirmations:
                confirmations.append(tmp_usr.email)
            tmp_usr = tmp_usr.linear_refer.refer
            linears.append(tmp_usr.email)
        confirmations.sort()
        if (refers == confirmations) if strict else len(confirmations) > 0:
            print(f'Approved with {len(confirmations)} confirmations')
        else:
            linears = "\n".join(list(reversed(linears)))
            print(f'!!! Rejected with {len(confirmations)} confirmations\n\nRefers:\n{linears}')
            return
    if interactive:
        confirm = input('Checks passed. Change email [Y/n]?')
    else:
        confirm = "y"
    if confirm in ["Y", "y"]:
        print("Saving...")
        u.email = to_email
        u.save()
    else:
        print("Change aborted. Exiting")
        return
