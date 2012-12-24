import inspect


class type_signature():
    def __init__(self, **kwsignature):
        self.kwsignature = kwsignature

    def __call__(self, f):
        print "Keyword Signature", self.kwsignature
        def wrapped_f(*args):
            print "Args to f:", args
        return wrapped_f


class precondition():
    pass

class postcondition():
    pass


# TO BE REMOVED -- TESTING ONLY
def test():
    @type_signature(something=str)
    def say(something):
        print something

    say("Hello")

if __name__ == '__main__':
    test()
