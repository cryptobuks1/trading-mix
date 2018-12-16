#lang racket
(require "poly-matrix.rkt")
(require plot/pict)
(require db)
(require "data.rkt")

(define (s-curve-data start end)
  (define *db*
    (sqlite3-connect #:database
                     "data/ohcl-2018-08-22-00:17:13.sqlite"))
  (date-range *db*
              start
              end))

(define (extract data)
  (values (map (lambda (v)(vector-ref v 0)) data)
          (map (lambda (v)(vector-ref v 1)) data)))

(define (plot-top-of-s)
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

(define (fit-top-of-s)
  (define *db*
    (sqlite3-connect #:database
                     "data/ohcl-2018-08-22-00:17:13.sqlite"))
  (define s-curve-data (date-range *db*
                                   '(0 50 18 21 8 2018)
                                   '(0 20 20 21 8 2018)))
  (define xs (map (lambda (v)(vector-ref v 0)) s-curve-data))
  (define ys (map (lambda (v)(vector-ref v 1)) s-curve-data))
  (fit xs ys 2))


(define (plot-full-s-curve-data)
  (let*-values ([(data) (s-curve-data '(0 50 18 21 8 2018)
                                      '(0 20 21 21 8 2018))]
                [(x y) (extract data)])
    (plot (list (points   (map vector x y))
                (function (poly (fit x y 2)))))))

(define (fit-full-s-curve-data)
  (let*-values ([(data) (s-curve-data '(0 50 18 21 8 2018)
                                      '(0 20 21 21 8 2018))]
                [(x y) (extract data)])
    (fit x y 2)))


(define (x-for-max-reducer fitf x a)
  (if (< (fitf a)
         (fitf x))
      x
      a))

(define (find-x-for-max-y fitf xs)
  (foldl ((curry x-for-max-reducer) fitf)
         (car xs)
         xs))


(define (x-for-max-y)
  (let*-values ([(data) (s-curve-data '(0 50 18 21 8 2018)
                                      '(0 20 20 21 8 2018))]
                [(xs ys) (extract data)]
                [(fitf) (poly (fit xs ys 2))])
    (find-x-for-max-y fitf xs)))
