# @Time    : 2018/3/19 8:41
# @Author  : Niyoufa


import asyncio
import aiomysql

import tormysql
from tornado.ioloop import IOLoop
from tornado import gen

@gen.coroutine
def test():
    pool = tormysql.ConnectionPool(
        max_connections=20,  # max open connections
        idle_seconds=7200,  # conntion idle timeout time, 0 is not timeout
        wait_connection_timeout=3,  # wait connection timeout
        host="180.96.11.78",
        port=3309,
        user="ucenter",
        passwd="!Crawler@2015#",
        db="imonitor",
        charset="utf8"
    )
    with (yield pool.Connection()) as conn:
        try:
            with conn.cursor() as cursor:
                yield cursor.execute("select count(*) from aegis_user;")
                datas = cursor.fetchall()
                print(datas)
        except:
            pass
    yield pool.close()

if __name__ == "__main__":
    pass
    # loop = asyncio.get_event_loop()
    #
    # @asyncio.coroutine
    # def go():
    #     pool = yield from aiomysql.create_pool(host='180.96.11.78', port=3309,
    #                                            user='ucenter', password='!Crawler@2015#',
    #                                            db='imonitor', loop=loop)
    #
    #     with (yield from pool) as conn:
    #         cur = yield from conn.cursor()
    #         yield from cur.execute("select count(*) from aegis_user;")
    #         print(cur.description)
    #         (r,) = yield from cur.fetchone()
    #         print(r)
    #     pool.close()
    #     yield from pool.wait_closed()
    #
    # loop.run_until_complete(go())

    pool = tormysql.ConnectionPool(
        max_connections=20,  # max open connections
        idle_seconds=7200,  # conntion idle timeout time, 0 is not timeout
        wait_connection_timeout=3,  # wait connection timeout
        host="180.96.11.78",
        port=3309,
        user="ucenter",
        passwd="!Crawler@2015#",
        db="imonitor",
        charset="utf8"
    )

    @gen.coroutine
    def test():
        with (yield pool.Connection()) as conn:
            try:
                with conn.cursor() as cursor:
                    yield cursor.execute("select count(*) from aegis_user;")
                    datas = cursor.fetchall()
                    print(datas)
            except:
                pass
        yield pool.close()

    ioloop = IOLoop.instance()
    ioloop.run_sync(test)