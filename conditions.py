""" conditions: a Python module providing decorators for type signatures, pre- and postconditions.

    This module implements the following decorator classes:
        * type_signature - type-checking function inputs
        * precondition   - checking validity of function inputs
        * postcondition  - checking validity of function outputs

    Author: Laurence Joseph Smith
    GitHub: Sourceless
    Email : laurence@sourceless.org
            ljs551@york.ac.uk
"""

import inspect

class type_signature():
    """ A decorator used for type-checking.
        
        This class implements a decorator for type signatures, in order
        to check types of function inputs. Usual use:

            @type_signature(argument1=type, argument2=type)
            def func(argument1, argument2):
                ...
        
        Ensure the keywords used in the type signature match the argument
        names for the function, or they won't be checked.

        A TypeError will be raised if the types of the arguments func is
        called with don't match the types given as arguments to the 
        decorator.

        If you want to allow more than one type for a given argument, pass
        in a tuple of types as opposed to a plain old type:

            @type_signature(argument1=(type1, type2, type3))
            def func(argument1):
                ...

        This way argument1 in the above function may only be of the types
        in the tuple (else a TypeError will be raised, as previously).

        The current limitation is that you can only have one type signature
        per function (you may however be able to stack similar signatures).
        This functionality may be implemented in future if there are any
        uses for it. Contact me to let me know if you have one.

    """

    def __init__(self, **signature):
        """ Initialise by storing signature kwargs as instance attribute """
        self.signature = signature # By using keyword args we can match
                                   # the arg names, meaning we can use
                                   # dicts without worrying too much

    def __call__(self, f):
        """ Check argument types given for f against types stored in signature,
            raise a TypeError if a type does not match.
        """
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

                if not argtype in rule: # There's an incorrect type around here
                    raise TypeError("Incorrect argument type for `" + key + 
                                    "` in `" + f.__name__ + "()`: should be " + 
                                    ("one of " if len(rule) > 1 else "")  + 
                                    ', '.join([ruletype.__name__ for ruletype in rule]) + 
                                    " not " + argtype.__name__)
            
            # And finally call the function
            return f(*args, **kwargs) # Function can still fail but at this point
                                      # That's the interpreter's responsibility
        
        return wrapped_f


class precondition():
    def __init__(self, **conditions):
        self.conditions = conditions

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            argspec = inspect.getargspec(f).args
            argspec = dict(zip(argspec, args))
            argspec.update(kwargs)
            
            for key in argspec.keys():
                if key not in self.conditions:
                    del argspec[key]

            for key, argument in argspec.iteritems():
                if type(self.conditions[key]) is not tuple:
                    self.conditions[key] = (self.conditions[key],)

                print self.conditions[key]
                for validation_func in self.conditions[key]:
                    if not validation_func(argument):
                        raise ValueError("Invalid input for " + key + " in " + 
                                         f.__name__ + ".")
            return f(*args, **kwargs)
        return wrapped_f


class postcondition():
    pass


# TO BE REMOVED -- TESTING ONLY
def test():
    @type_signature(nothing=list)
    @precondition(something=(lambda s: len(s) > 5))
    def say(something, nothing=[]):
        print something
        return len(something)

    a_string = "Hey lookie words"
    not_a_string = 42
    say(a_string)
    #say(not_a_string)
    say(a_string, nothing=6)
    print say("")

if __name__ == '__main__':
    test()
