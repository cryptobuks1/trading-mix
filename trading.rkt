#lang racket
(require plot/pict)
(require db)
(require racket/class)
(require racket/date)
(require data-frame)
(define *db*
  (sqlite3-connect #:database
                   "data/ohcl-2018-08-22-00:17:13.sqlite"))
(define rows (query-rows *db* "select time, open from ohlc order by time asc"))
(define start-s-curve (find-seconds	0 45 20 22 8 2018))
(define end-s-curve (find-seconds	0 20 23 22 8 2018))
(define start-from-python 1534880537.142857)
(define end-from-python 1534885655.510204)
(define start-from-python (- 1534880537.142857 2400))
(define end-from-python 1534885655.510204)
(define s-curve-data  (query-rows *db*
                                  "select time,open from ohlc where time >= $1 and time <= $2 order by time asc"
                                  start-from-python end-from-python))
(define xs (map (lambda (row)
                  (* 1.0 (vector-ref row 0)))
                s-curve-data))
(define ys (map (lambda (row)
                  (* 1.0 (vector-ref row 1)))
                s-curve-data))
(define fitf(line-fit xs ys))

(define fitf (df-least-squares-fit df "xs" "ys" #:mode 'polynomial  #:polynomial-degree 5))

(define ynew (map fitf xs))
;; (plot-new-window? #t)
(plot (lines rows))
