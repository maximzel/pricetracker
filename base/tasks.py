from __future__ import absolute_import, unicode_literals
from celery import shared_task
from base.parser_perek import parse_perek
from base.parser_utko import parse_utko
from base.utilities import preparse_to_available


@shared_task
def update_db():
    parse_perek()
    parse_utko()
    preparse_to_available()
