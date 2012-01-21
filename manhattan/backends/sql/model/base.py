from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

from . import meta


class _Base(object):

    @classmethod
    def find_or_create(cls, **kw):
        try:
            rec = meta.Session.query(cls).filter_by(**kw).one()
        except NoResultFound:
            rec = cls(**kw)
            meta.Session.add(rec)
        return rec


Base = declarative_base(metadata=meta.metadata, cls=_Base)