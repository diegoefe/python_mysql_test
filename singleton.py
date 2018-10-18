import threading

class  Singleton (object):
    instance_ = None
    semaphore_ = threading.Semaphore( 1 )
    def __new__(cls, *args, **kargs):
        if cls.instance_ is None:
            cls.semaphore_.acquire()
            if cls.instance_ is None:
                cls.instance_ = object.__new__(cls, *args, **kargs)
            cls.semaphore_.release()
        return cls.instance_

