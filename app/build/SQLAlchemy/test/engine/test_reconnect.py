from sqlalchemy.testing import eq_, assert_raises, assert_raises_message
import time
import weakref
from sqlalchemy import select, MetaData, Integer, String, pool, create_engine
from sqlalchemy.testing.schema import Table, Column
import sqlalchemy as tsa
from sqlalchemy import testing
from sqlalchemy.testing import engines
from sqlalchemy.testing.util import gc_collect
from sqlalchemy import exc
from sqlalchemy.testing import fixtures
from sqlalchemy.testing.engines import testing_engine

class MockError(Exception):
    pass

class MockDisconnect(MockError):
    pass

class MockDBAPI(object):
    def __init__(self):
        self.paramstyle = 'named'
        self.connections = weakref.WeakKeyDictionary()
    def connect(self, *args, **kwargs):
        return MockConnection(self)
    def shutdown(self, explode='execute'):
        for c in self.connections:
            c.explode = explode
    Error = MockError

class MockConnection(object):
    def __init__(self, dbapi):
        dbapi.connections[self] = True
        self.explode = ""
    def rollback(self):
        if self.explode == 'rollback':
            raise MockDisconnect("Lost the DB connection on rollback")
        if self.explode == 'rollback_no_disconnect':
            raise MockError(
                "something broke on rollback but we didn't lose the connection")
        else:
            return
    def commit(self):
        pass
    def cursor(self):
        return MockCursor(self)
    def close(self):
        pass

class MockCursor(object):
    def __init__(self, parent):
        self.explode = parent.explode
        self.description = ()
        self.closed = False
    def execute(self, *args, **kwargs):
        if self.explode == 'execute':
            raise MockDisconnect("Lost the DB connection on execute")
        elif self.explode in ('execute_no_disconnect', ):
            raise MockError(
                "something broke on execute but we didn't lose the connection")
        elif self.explode in ('rollback', 'rollback_no_disconnect'):
            raise MockError(
                "something broke on execute but we didn't lose the connection")
        elif args and "select" in args[0]:
            self.description = [('foo', None, None, None, None, None)]
        else:
            return
    def fetchall(self):
        if self.closed:
            raise MockError("cursor closed")
        return []
    def fetchone(self):
        if self.closed:
            raise MockError("cursor closed")
        return None
    def close(self):
        self.closed = True

db, dbapi = None, None
class MockReconnectTest(fixtures.TestBase):
    def setup(self):
        global db, dbapi
        dbapi = MockDBAPI()

        # note - using straight create_engine here
        # since we are testing gc
        db = create_engine(
                    'postgresql://foo:bar@localhost/test',
                    module=dbapi, _initialize=False)

        # monkeypatch disconnect checker
        db.dialect.is_disconnect = lambda e, conn, cursor: isinstance(e, MockDisconnect)

    def teardown(self):
        db.dispose()

    def test_reconnect(self):
        """test that an 'is_disconnect' condition will invalidate the
        connection, and additionally dispose the previous connection
        pool and recreate."""

        pid = id(db.pool)

        # make a connection

        conn = db.connect()

        # connection works

        conn.execute(select([1]))

        # create a second connection within the pool, which we'll ensure
        # also goes away

        conn2 = db.connect()
        conn2.close()

        # two connections opened total now

        assert len(dbapi.connections) == 2

        # set it to fail

        dbapi.shutdown()
        try:
            conn.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError:
            pass

        # assert was invalidated

        assert not conn.closed
        assert conn.invalidated

        # close shouldnt break

        conn.close()
        assert id(db.pool) != pid

        # ensure all connections closed (pool was recycled)

        gc_collect()
        assert len(dbapi.connections) == 0
        conn = db.connect()
        conn.execute(select([1]))
        conn.close()
        assert len(dbapi.connections) == 1

    def test_invalidate_trans(self):
        conn = db.connect()
        trans = conn.begin()
        dbapi.shutdown()
        try:
            conn.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError:
            pass

        # assert was invalidated

        gc_collect()
        assert len(dbapi.connections) == 0
        assert not conn.closed
        assert conn.invalidated
        assert trans.is_active
        assert_raises_message(
            tsa.exc.StatementError,
            "Can't reconnect until invalid transaction is rolled back",
            conn.execute, select([1])
        )
        assert trans.is_active
        try:
            trans.commit()
            assert False
        except tsa.exc.InvalidRequestError, e:
            assert str(e) \
                == "Can't reconnect until invalid transaction is "\
                "rolled back"
        assert trans.is_active
        trans.rollback()
        assert not trans.is_active
        conn.execute(select([1]))
        assert not conn.invalidated
        assert len(dbapi.connections) == 1

    def test_conn_reusable(self):
        conn = db.connect()

        conn.execute(select([1]))

        assert len(dbapi.connections) == 1

        dbapi.shutdown()

        assert_raises(
            tsa.exc.DBAPIError,
            conn.execute, select([1])
        )

        assert not conn.closed
        assert conn.invalidated

        # ensure all connections closed (pool was recycled)
        gc_collect()
        assert len(dbapi.connections) == 0

        # test reconnects
        conn.execute(select([1]))
        assert not conn.invalidated
        assert len(dbapi.connections) == 1

    def test_invalidated_close(self):
        conn = db.connect()

        dbapi.shutdown()

        assert_raises(
            tsa.exc.DBAPIError,
            conn.execute, select([1])
        )

        conn.close()
        assert conn.closed
        assert conn.invalidated
        assert_raises_message(
            tsa.exc.StatementError,
            "This Connection is closed",
            conn.execute, select([1])
        )

    def test_noreconnect_execute_plus_closewresult(self):
        conn = db.connect(close_with_result=True)

        dbapi.shutdown("execute_no_disconnect")

        # raises error
        assert_raises_message(
            tsa.exc.DBAPIError,
            "something broke on execute but we didn't lose the connection",
            conn.execute, select([1])
        )

        assert conn.closed
        assert not conn.invalidated

    def test_noreconnect_rollback_plus_closewresult(self):
        conn = db.connect(close_with_result=True)

        dbapi.shutdown("rollback_no_disconnect")

        # raises error
        assert_raises_message(
            tsa.exc.DBAPIError,
            "something broke on rollback but we didn't lose the connection",
            conn.execute, select([1])
        )

        assert conn.closed
        assert not conn.invalidated

        assert_raises_message(
            tsa.exc.StatementError,
            "This Connection is closed",
            conn.execute, select([1])
        )

    def test_reconnect_on_reentrant(self):
        conn = db.connect()

        conn.execute(select([1]))

        assert len(dbapi.connections) == 1

        dbapi.shutdown("rollback")

        # raises error
        assert_raises_message(
            tsa.exc.DBAPIError,
            "Lost the DB connection on rollback",
            conn.execute, select([1])
        )

        assert not conn.closed
        assert conn.invalidated

    def test_reconnect_on_reentrant_plus_closewresult(self):
        conn = db.connect(close_with_result=True)

        dbapi.shutdown("rollback")

        # raises error
        assert_raises_message(
            tsa.exc.DBAPIError,
            "Lost the DB connection on rollback",
            conn.execute, select([1])
        )

        assert conn.closed
        assert conn.invalidated

        assert_raises_message(
            tsa.exc.StatementError,
            "This Connection is closed",
            conn.execute, select([1])
        )

    def test_check_disconnect_no_cursor(self):
        conn = db.connect()
        result = conn.execute("select 1")
        result.cursor.close()
        conn.close()
        assert_raises_message(
            tsa.exc.DBAPIError,
            "cursor closed",
            list, result
        )

class CursorErrTest(fixtures.TestBase):

    def setup(self):
        global db, dbapi

        class MDBAPI(MockDBAPI):
            def connect(self, *args, **kwargs):
                return MConn(self)

        class MConn(MockConnection):
            def cursor(self):
                return MCursor(self)

        class MCursor(MockCursor):
            def close(self):
                raise Exception("explode")

        dbapi = MDBAPI()

        db = testing_engine(
                    'postgresql://foo:bar@localhost/test',
                    options=dict(module=dbapi, _initialize=False))

    def test_cursor_explode(self):
        conn = db.connect()
        result = conn.execute("select foo")
        result.close()
        conn.close()

    def teardown(self):
        db.dispose()

engine = None
class RealReconnectTest(fixtures.TestBase):
    def setup(self):
        global engine
        engine = engines.reconnecting_engine()

    def teardown(self):
        engine.dispose()

    @testing.fails_on('+informixdb',
                      "Wrong error thrown, fix in informixdb?")
    def test_reconnect(self):
        conn = engine.connect()

        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.closed

        engine.test_shutdown()

        try:
            conn.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError, e:
            if not e.connection_invalidated:
                raise

        assert not conn.closed
        assert conn.invalidated

        assert conn.invalidated
        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.invalidated

        # one more time
        engine.test_shutdown()
        try:
            conn.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError, e:
            if not e.connection_invalidated:
                raise
        assert conn.invalidated
        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.invalidated

        conn.close()

    def test_multiple_invalidate(self):
        c1 = engine.connect()
        c2 = engine.connect()

        eq_(c1.execute(select([1])).scalar(), 1)

        p1 = engine.pool
        engine.test_shutdown()

        try:
            c1.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError, e:
            assert e.connection_invalidated

        p2 = engine.pool

        try:
            c2.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError, e:
            assert e.connection_invalidated

        # pool isn't replaced
        assert engine.pool is p2


    def test_ensure_is_disconnect_gets_connection(self):
        def is_disconnect(e, conn, cursor):
            # connection is still present
            assert conn.connection is not None
            # the error usually occurs on connection.cursor(),
            # though MySQLdb we get a non-working cursor.
            # assert cursor is None

        engine.dialect.is_disconnect = is_disconnect
        conn = engine.connect()
        engine.test_shutdown()
        assert_raises(
            tsa.exc.DBAPIError,
            conn.execute, select([1])
        )

    def test_rollback_on_invalid_plain(self):
        conn = engine.connect()
        trans = conn.begin()
        conn.invalidate()
        trans.rollback()

    @testing.requires.two_phase_transactions
    def test_rollback_on_invalid_twophase(self):
        conn = engine.connect()
        trans = conn.begin_twophase()
        conn.invalidate()
        trans.rollback()

    @testing.requires.savepoints
    def test_rollback_on_invalid_savepoint(self):
        conn = engine.connect()
        trans = conn.begin()
        trans2 = conn.begin_nested()
        conn.invalidate()
        trans2.rollback()

    def test_invalidate_twice(self):
        conn = engine.connect()
        conn.invalidate()
        conn.invalidate()

    def test_explode_in_initializer(self):
        engine = engines.testing_engine()
        def broken_initialize(connection):
            connection.execute("select fake_stuff from _fake_table")

        engine.dialect.initialize = broken_initialize

        # raises a DBAPIError, not an AttributeError
        assert_raises(exc.DBAPIError, engine.connect)

        # dispose connections so we get a new one on
        # next go
        engine.dispose()

        p1 = engine.pool

        def is_disconnect(e, conn, cursor):
            return True

        engine.dialect.is_disconnect = is_disconnect

        # invalidate() also doesn't screw up
        assert_raises(exc.DBAPIError, engine.connect)

        # pool was recreated
        assert engine.pool is not p1

    @testing.fails_on('+informixdb',
                      "Wrong error thrown, fix in informixdb?")
    def test_null_pool(self):
        engine = \
            engines.reconnecting_engine(options=dict(poolclass=pool.NullPool))
        conn = engine.connect()
        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.closed
        engine.test_shutdown()
        try:
            conn.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError, e:
            if not e.connection_invalidated:
                raise
        assert not conn.closed
        assert conn.invalidated
        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.invalidated

    @testing.fails_on('+informixdb',
                      "Wrong error thrown, fix in informixdb?")
    def test_close(self):
        conn = engine.connect()
        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.closed

        engine.test_shutdown()

        try:
            conn.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError, e:
            if not e.connection_invalidated:
                raise

        conn.close()
        conn = engine.connect()
        eq_(conn.execute(select([1])).scalar(), 1)

    @testing.fails_on('+informixdb',
                      "Wrong error thrown, fix in informixdb?")
    def test_with_transaction(self):
        conn = engine.connect()
        trans = conn.begin()
        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.closed
        engine.test_shutdown()
        try:
            conn.execute(select([1]))
            assert False
        except tsa.exc.DBAPIError, e:
            if not e.connection_invalidated:
                raise
        assert not conn.closed
        assert conn.invalidated
        assert trans.is_active
        assert_raises_message(
            tsa.exc.StatementError,
            "Can't reconnect until invalid transaction is "\
                "rolled back",
            conn.execute, select([1])
        )
        assert trans.is_active
        try:
            trans.commit()
            assert False
        except tsa.exc.InvalidRequestError, e:
            assert str(e) \
                == "Can't reconnect until invalid transaction is "\
                "rolled back"
        assert trans.is_active
        trans.rollback()
        assert not trans.is_active
        assert conn.invalidated
        eq_(conn.execute(select([1])).scalar(), 1)
        assert not conn.invalidated

class RecycleTest(fixtures.TestBase):

    def test_basic(self):
        for threadlocal in False, True:
            engine = engines.reconnecting_engine(
                        options={'pool_threadlocal': threadlocal})

            conn = engine.contextual_connect()
            eq_(conn.execute(select([1])).scalar(), 1)
            conn.close()

            # set the pool recycle down to 1.
            # we aren't doing this inline with the
            # engine create since cx_oracle takes way
            # too long to create the 1st connection and don't
            # want to build a huge delay into this test.

            engine.pool._recycle = 1

            # kill the DB connection
            engine.test_shutdown()

            # wait until past the recycle period
            time.sleep(2)

            # can connect, no exception
            conn = engine.contextual_connect()
            eq_(conn.execute(select([1])).scalar(), 1)
            conn.close()

meta, table, engine = None, None, None
class InvalidateDuringResultTest(fixtures.TestBase):
    def setup(self):
        global meta, table, engine
        engine = engines.reconnecting_engine()
        meta = MetaData(engine)
        table = Table('sometable', meta,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)))
        meta.create_all()
        table.insert().execute(
            [{'id':i, 'name':'row %d' % i} for i in range(1, 100)]
        )

    def teardown(self):
        meta.drop_all()
        engine.dispose()

    @testing.fails_on('+cymysql',
                      "Buffers the result set and doesn't check for "
                      "connection close")
    @testing.fails_on('+pymysql',
                      "Buffers the result set and doesn't check for "
                      "connection close")
    @testing.fails_on('+mysqldb',
                      "Buffers the result set and doesn't check for "
                      "connection close")
    @testing.fails_on('+pg8000',
                      "Buffers the result set and doesn't check for "
                      "connection close")
    @testing.fails_on('+informixdb',
                      "Wrong error thrown, fix in informixdb?")
    def test_invalidate_on_results(self):
        conn = engine.connect()
        result = conn.execute('select * from sometable')
        for x in xrange(20):
            result.fetchone()
        engine.test_shutdown()
        try:
            print 'ghost result: %r' % result.fetchone()
            assert False
        except tsa.exc.DBAPIError, e:
            if not e.connection_invalidated:
                raise
        assert conn.invalidated

