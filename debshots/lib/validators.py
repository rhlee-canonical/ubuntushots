# -*- coding: utf-8 -*-
#
# Formencode validators

import formencode
from debshots import model

# Formencode validators
class ValidatorDebianPackage(formencode.FancyValidator):
    """formencode validator that makes sure a certain Debian package exists (by its name)"""
    messages = {
            'not_exists' : \
                u'There is no Debian package with that name.',
            }

    def _to_python(self, value, state):
        package = model.Package.q().filter_by(name=value).first()
        if not package:
            raise formencode.Invalid(self.message("not_exists", state), value, state)
        return package
