#!/usr/bin/env python3

import pytest

import dope

def _genuid():
    uid = 0
    while True:
        yield uid
        uid += 1


_ITERUID = _genuid()
_URL = "sqlite:///test_decorator.db"
_TIMEOUT = 1.5

config = dope.DeferredTrove(
    sql_url=_URL,
    sql_timeout=_TIMEOUT,
    uid=dope.Factory(lambda: next(_ITERUID)),
)


class Db(object):
    @dope.inject(url=config["sql_url"], timeout=config["sql_timeout"])
    def __init__(self, url, timeout):
       self.url = url
       self.timeout = timeout

    def __repr__(self):
       return "{}(url={!r}, timeout={!r})".format(self.__class__.__name__, self.url, self.timeout)

    def __eq__(self, other):
       return self.url == other.url and self.timeout == other.timeout


class Result(object):
    @dope.inject(backend=config["backend"], uid=config["uid"])
    def __init__(self, backend, uid):
       self.backend = backend
       self.uid = uid

    def __repr__(self):
       return "{}(backend={!r}, uid={!r})".format(self.__class__.__name__, self.backend, self.uid)


config["backend"] = dope.Factory(lambda : Db())

def test_default_constructor_Db():
    db = Db()
    assert db.url == _URL
    assert db.timeout == _TIMEOUT

def test_default_constructor_Result():
    result0 = Result()
    assert result0.backend == Db()
    assert result0.uid == 0
    result1 = Result()
    assert result1.uid == 1
    result2 = Result()
    assert result2.uid == 2
    
def test_all_parameters_set_positionally():
    result = Result(Db("a", 1.2), 345)
    assert result.backend.url == "a"
    assert result.backend.timeout == 1.2
    assert result.uid == 345
    
def test_all_parameters_set_by_keyword():
    result0 = Result(backend=Db(url="a", timeout=1.2), uid=345)
    assert result0.backend.url == "a"
    assert result0.backend.timeout == 1.2
    assert result0.uid == 345
    
def test_partial_set():
    result0 = Result(uid=456)
    assert result0.backend.url == _URL
    assert result0.backend.timeout == _TIMEOUT
    assert result0.uid == 456
    
