#lang racket
(require "poly-matrix.rkt")
(require plot/pict)
(require db)
(require "data.rkt")
(require "plot.rkt")

(define (s-curve-data start end)
  (define *db*
    (sqlite3-connect #:database
                     "data/ohcl-2018-08-22-00:17:13.sqlite"))
  (date-range *db*
              start
              end))

(define top-of-s (s-curve-data '(0 50 18 21 8 2018)
                               '(0 20 20 21 8 2018)))

(define bottom-of-s (s-curve-data '(0 20 19 21 8 2018)
                                  '(0 20 21 21 8 2018)))

(define full-s-curve (s-curve-data '(0 50 18 21 8 2018)
                                   '(0 20 21 21 8 2018)))


(define (plot-top-of-s)
  (plot-with-x-as-time (list (points top-of-s)
                             (function (fitf top-of-s)))))

(define (plot-bottom-of-s)
  (plot-with-x-as-time (list (points bottom-of-s)
                             (function (fitf bottom-of-s)))))

(define (fit-top-of-s)
  (fit-data top-of-s))


(define (fit-bottom-of-s)
  (fit-data bottom-of-s))


(define (plot-full-s-curve-data)
  (plot-with-x-as-time (list (points full-s-curve)
                             (function (fitf full-s-curve)))))


(define (fit-full-s-curve-data)
  (fit-data full-s-curve))
