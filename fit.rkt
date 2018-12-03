#lang racket

(require db)
(require data-frame)

(define *db*
  (sqlite3-connect #:database
                   "data/ohcl-2018-08-22-00:17:13.sqlite"))

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

(define df (make-data-frame))

(define dxs (make-series "xs" #:data (apply vector xs)))
(define dys (make-series "ys" #:data (apply vector ys)))

(df-add-series df dxs)
(df-add-series df dys)

(define fitf (df-least-squares-fit df "xs" "ys" #:mode 'polynomial))
