#lang racket
(require db)
(require racket/date)
(provide date-range)

(define (date-range connection start end)

  (define start-s-curve (+ 3600 (apply find-seconds start)))
  (define end-s-curve (+ 3600 (apply find-seconds end)))
  (query-rows connection
              "select time,open from ohlc where time >= $1 and time <= $2 order by time asc"
              start-s-curve end-s-curve))

(module+ test
  (define *db*
    (sqlite3-connect #:database
                     "data/ohcl-2018-08-22-00:17:13.sqlite"))
  (date-range *db*
              '(0 45 20 21 8 2018)
              '(0 20 23 21 8 2018)))
