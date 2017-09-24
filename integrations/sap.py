class SapIntegration(object):

    events = {}
    
    def __init__(self):
        pass

    def issue(self, issued_event, *issued_event_args):
        for event in self.events:
            if issued_event == event:
                self.events[issued_event](*issued_event_args)
                

    def event(self, route):
        def _event(func, route=route, self=self):
            self.events[route] = func

        return _event
