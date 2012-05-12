from pypy.rlib import jit


class ExecutionContext(object):
    def __init__(self, space):
        self.space = space
        self.topframeref = jit.vref_None

    def enter(self, frame):
        frame.backref = self.topframeref
        self.topframeref = jit.virtual_ref(frame)

    def leave(self, frame, got_exception):
        frame_vref = self.topframeref
        self.topframeref = frame.backref
        if frame.escaped or got_exception:
            back = frame.backref()
            if back is not None:
                back.escaped = True
            frame_vref()
        jit.virtual_ref_finish(frame_vref, frame)
