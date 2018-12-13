#lang racket
(require "poly-matrix.rkt")
(require plot/pict)
(require db)
(require "data.rkt")

(define (2018-8-21-18-21)
  (define *db*
    (sqlite3-connect #:database
                     "data/ohcl-2018-08-22-00:17:13.sqlite"))
  (define s-curve-data (date-range *db*
                                   '(0 50 18 21 8 2018)
                                   '(0 20 20 21 8 2018)))
  (define xs (map (lambda (v)(vector-ref v 0)) s-curve-data))
  (define ys (map (lambda (v)(vector-ref v 1)) s-curve-data))
  (plot (list (points   (map vector xs ys))
              (function (poly (fit xs ys 2))))))
