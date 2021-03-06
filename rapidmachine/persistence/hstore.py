# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .persistence import Persistence


def untypeify(sql):
    return sql.replace("::timestamp", "")


class HstorePersistence(Persistence):  # pragma: no cover

    """
    PostgreSQL hstore persistence adapter.
    To use, execute `CREATE EXTENSION hstore;` on the database from the psql
    shell and create a table with id and an hstore, like that:
    `CREATE TABLE test (id serial PRIMARY KEY, data hstore);`
    Pass the hstore column name as the column argument if it isn't "data".
    """

    def __init__(self, conn, table, column="data"):
        import psycopg2.extras
        self.conn = conn
        psycopg2.extras.register_hstore(self.conn)
        self.cur = conn.cursor()
        self.table = table
        self.column = column

    def create(self, params):
        sql = self.cur.mogrify("INSERT INTO " + self.table + \
                " (" + self.column + ") VALUES (%s)", (params,))
        sql = untypeify(sql)
        self.cur.execute(sql)
        self.conn.commit()
        return self.read_one(params)

    def read_one(self, query, fields=None):
        c = self.read_many(query, fields=fields, limit=1)
        if len(c) > 0:
            return c[0]
        return None

    def read_many(self, query, fields=None, skip=None, limit=None):
        sql = "SELECT id, " + self.column + " FROM " + self.table + \
                " WHERE (" + self.column + " @> %s)"
        if limit:
            sql += " LIMIT " + str(int(limit))
        if skip:
            sql += " OFFSET " + str(int(skip))

        sql = untypeify(self.cur.mogrify(sql, (query,)))
        self.cur.execute(sql)
        c = []
        for d in self.cur:
            data = d[1]
            data["id"] = d[0]
            if fields:
                for field in list(data.iterkeys()):
                    if field not in fields:
                        del data[field]
            c.append(data)
        return c

    def replace(self, query, params):
        self.cur.execute("UPDATE " + self.table + " SET " + self.column + \
                " = (%s) WHERE (" + self.column + " @> %s)", (params, query))
        self.conn.commit()
        return self.read_one(params)

    def update(self, query, params):
        self.cur.execute("UPDATE " + self.table + " SET " + self.column + \
                " = " + self.column + " || (%s) WHERE (" + self.column + \
                " @> %s)", (params, query))
        self.conn.commit()
        return self.read_one(params)

    def delete(self, query):
        self.cur.execute("DELETE FROM " + self.table + \
                " WHERE (" + self.column + " @> %s)", (query,))
        self.conn.commit()
        return True

    def count(self):
        self.cur.execute("SELECT count(*) FROM %s" % self.table)
        return int(self.cur.next()[0])
