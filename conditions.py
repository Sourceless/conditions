import inspect


class type_signature():
    def __init__(self, **signature):
        self.signature = signature # By using keyword args we can match
                                   # the arg names, meaning we can use
                                   # dicts without worrying too much

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            argspec = inspect.getargspec(f).args # Get the names of f's args
            
            # Bind the arg names and arguments into a dict.
            # *SHOULD* preserve order and get rid of unused keyword args
            argspec = dict(zip(argspec, args))
            argspec.update(kwargs) # Make sure to add/update missed keyword args
            
            # Avoid KeyErrors by removing args that don't need to be checked
            for key in argspec.keys():
                if key not in self.signature:
                    del argspec[key]

            # Run through the rules in the signature.
            for key, value in argspec.iteritems():
                argtype = type(argspec[key])
                rule = self.signature[key]
                
                if type(rule) is not tuple: # convert single type vals to one-element tuples
                    rule = (rule,)          # to simplify if below. Dirty.

                if not argtype in rule: # The type doesn't match pne in the signature
                    raise TypeError("Incorrect argument type for `" + key + "` in `" + f.__name__ + "()`: should be " + ("one of " if len(rule) > 1 else "")  + ', '.join([ruletype.__name__ for ruletype in rule]) + " not " + argtype.__name__)
            
            # And finally call the function
            f(*args, **kwargs) # If the KeyError takes place, this will 
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
    #say(not_a_string)
    say(a_string, nothing=6)

if __name__ == '__main__':
    test()
