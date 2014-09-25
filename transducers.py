from itertools import chain


def mapper(f):
    def tducer(reducer):
        def reduce_applier(result, item):
            return reducer(result, f(item))
        return reduce_applier
    return tducer


def filterer(f):
    def tducer(reducer):
        def reduce_applier(result, item):
            return reducer(result, item) if f(item) else result
        return reduce_applier
    return tducer


def transduce(f, builder, start, coll):
    return reduce(f(builder), coll, start)


def sequence(f, data):
    if isinstance(data, list):
        return transduce(f, lambda x, y: x + [y], [], data)
    elif isinstance(data, tuple):
        return transduce(f, lambda x, y: x + (y,), tuple(), data)
    elif isinstance(data, dict):
        return transduce(f, lambda x, y: x + (y,), tuple(), data)
    elif hasattr(data, 'next'):
        return transduce(f, lambda x, y: chain(x, iter((y,))), iter(tuple()), data)
    else:
        if(hasattr(data, '__append__') and hasattr(data, 'empty')):
            return transduce(f, data.append, data.empty(), data)
        else:
            raise ProtocolException(
                "Not implemented __append__ and __empty__ protocols for type: {}".format(type(data)))


def map(f, coll):
    return sequence(mapper(f), coll)


def filter(f, coll):
    return sequence(filterer(f), coll)


class ProtocolException(Exception):
    pass

