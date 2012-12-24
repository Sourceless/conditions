import inspect


class type_signature():
    def __init__(self, **signature):
        self.signature = signature

    def __call__(self, f):
        def wrapped_f(*args):
            argspec = inspect.getargspec(f)
            if argspec[2]:
                argspec = argspec[0] + argspec[2]
            else:
                argspec = argspec[0]
            argspec = dict(zip(argspec, args))

            try:
                for key, rule in self.signature.iteritems():
                    if type(rule) is not tuple:
                        rule = (rule,)
                    argtype = type(argspec[key])
                    if not argtype in rule:
                        raise TypeError("Incorrect argument type for `" + key + "` in `" + f.__name__ + "()`: should be " + ("one of " if len(rule) > 1 else "")  + ', '.join([ruletype.__name__ for ruletype in rule]) + " not " + argtype.__name__)
            except KeyError, e:
                pass
            f(*args) # If the KeyError takes place, this will 
                     # raise the 'takes at least x arguments' error,
                     # however if the argument type error is raised
                     # the function will exit
        
        return wrapped_f


class precondition():
    pass

class postcondition():
    pass


# TO BE REMOVED -- TESTING ONLY
def test():
    @type_signature(something=str)
    def say(something, nothing=[]):
        print something

    a_string = "Hey lookie words"
    not_a_string = 42
    say(a_string)
    say(not_a_string)

if __name__ == '__main__':
    test()
