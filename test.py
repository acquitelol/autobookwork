class thing:
    def __init__(self, thing1, thing2):
        self.thing1 = thing1
        self.thing2 = thing2
    
    def someOtherFunc(self):
        print(self.thing1)

thing('hi', 'hello')

thing.someOtherFunc()
