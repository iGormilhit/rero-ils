# -*- coding: utf-8 -*-
#
# This file is part of RERO ILS.
# Copyright (C) 2017 RERO.
#
# RERO ILS is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# RERO ILS is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RERO ILS; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""API for manipulating organisation."""


from functools import partial

from ..api import IlsRecord
from ..fetchers import id_fetcher
from ..libraries.api import LibrariesSearch, Library
from ..minters import id_minter
from ..providers import Provider
from .models import OrganisationIdentifier

# provider
OrganisationProvider = type(
    'OrganisationProvider',
    (Provider,),
    dict(identifier=OrganisationIdentifier, pid_type='org')
)
# minter
organisation_id_minter = partial(id_minter, provider=OrganisationProvider)
# fetcher
organisation_id_fetcher = partial(id_fetcher, provider=OrganisationProvider)


class Organisation(IlsRecord):
    """Organisation class."""

    minter = organisation_id_minter
    fetcher = organisation_id_fetcher
    provider = OrganisationProvider

    def get_libraries(self):
        """Get all libraries related to the organisation."""
        results = LibrariesSearch().source(['pid'])\
            .filter('term', organisation__pid=self.pid)\
            .scan()
        for library in results:
            yield Library.get_record_by_pid(library.pid)
