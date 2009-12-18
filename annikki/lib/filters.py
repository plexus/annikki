"""
A Genshi filter is a callable that, when called with a stream generator,
returns a new stream generator.
"""

from genshi.path import Path
from genshi.core import Attrs, QName
from genshi.core import END, START, TEXT, COMMENT

class HTMLFormErrors(object):   
    def __init__(self, errors=None):
        self.errors = errors

    def __call__(self, stream):
        tests = [[Path("//input[@name='%s']" % name).test(), error] for name, error in self.errors.items()]
        emit_msg = None
        for kind, data, pos in stream:
            for test, error in tests:
                if test((kind, data, pos), {}, {}):
                    tag, attrs = data
                    klz = attrs.get('class').split(' ') or []
                    klz.append('error')
                    attrs |= [('class', ' '.join(klz))]
                    data = (tag, attrs)
                    emit_msg = error
            if kind == END and emit_msg:
                yield kind, data, pos
                yield START, (QName('span'), Attrs([(QName('class'),'errormsg')])), pos
                yield TEXT, emit_msg, pos
                yield END, QName('span'), pos
                emit_msg = None
            else:
                yield kind, data, pos
            
