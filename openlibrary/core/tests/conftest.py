import os

def pytest_funcarg__dummy_crontabfile(request):
    "Creates a dummy crontab file that can be used for to try things"
    cronfile = os.tmpnam()
    ip = """* * * * * /bin/true
* * * * * /bin/true"""
    f = open(cronfile,"w")
    f.write(ip)
    f.close()
    request.addfinalizer(lambda : os.remove(cronfile))
    return cronfile
    
def pytest_funcarg__crontabfile(request):
    """Creates a file with an actual command that we can use to test
    running of cron lines"""
    if os.path.exists("/tmp/crontest"):
        os.unlink("/tmp/crontest")
    cronfile = os.tmpnam()
    ip = "* * * * * touch /tmp/crontest"
    f = open(cronfile,"w")
    f.write(ip)
    f.close()
    request.addfinalizer(lambda : os.remove(cronfile))
    return cronfile

def pytest_funcarg__counter(request):
    """Returns a decorator that will create a 'counted' version of the
    functions. The number of times it's been called is kept in the
    .invocations attribute"""
    def counter(fn):
        def _counted(*largs, **kargs):
            _counted.invocations += 1
            fn(*largs, **kargs)
        _counted.invocations = 0
        return _counted
    return counter

def pytest_funcarg__couchdb(request):
    "Returns a mock couchdb database"
    from openlibrary.mocks import mock_couchdb
    db = mock_couchdb.Database()    
    db.save({
            "_id": "_design/cases",
            "views": {
                "all": {
                    "map": "" +  
                    "def f(doc):\n" + 
                    "    if doc.get('type','') == 'case':\n"
                    "        yield doc['_id'], doc"
                    }
                }
            })
    return db



def pytest_funcarg__sequence(request):
    """Returns a function that can be called for sequence numbers
    similar to web.ctx.site.sequence.get_next"""
    t = (x for x in range(100))
    def seq_counter(*largs, **kargs):
        return t.next()
    import web
    # Clean up this mess to mock sequences
    web.ctx = lambda:0
    web.ctx.site = lambda:0
    web.ctx.site.seq = lambda: 0
    web.ctx.site.seq.next_value = seq_counter
    # Now run the test
    return seq_counter

