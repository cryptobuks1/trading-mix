#lang racket
(require db)
(define *db*
  (sqlite3-connect #:database
                   "data/ohcl-2018-08-22-00:17:13.sqlite"))
(define rows (query-rows *db* "select time, open from ohlc"))
