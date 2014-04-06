#!/usr/bin/python
# -*- coding: utf-8 -*-
import PySQLPool
  

if __name__ == "__main__":
  connection = PySQLPool.getNewConnection(username='root', password='password', host='localhost', db='sandyfiles')
  query = PySQLPool.getNewQuery(connection)
  query.QueryOne('SELECT VERSION()')
  print query.record
