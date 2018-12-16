#lang racket
(require math plot)

(provide poly fit fit-values)

(define xs '(0 1  2  3  4  5   6   7   8   9  10))
(define ys '(1 6 17 34 57 86 121 162 209 262 321))

(define (fit x y n)
  (define Y (->col-matrix y))
  (define V (vandermonde-matrix x (+ n 1)))
  (define VT (matrix-transpose V))
  (matrix->vector (matrix-solve (matrix* VT V) (matrix* VT Y))))

(define (fit-values xandy n)
  (let-values ([(x y) xandy])
    (fit x y n)))

(define ((poly v) x)
  (for/sum ([c v] [i (in-naturals)])
    (* c (expt x i))))


(module+ test
  (require db)
  (require "data.rkt")
  (define *db*
    (sqlite3-connect #:database
                     "data/ohcl-2018-08-22-00:17:13.sqlite"))
  (define s-curve-data (date-range *db*
                                   '(0 50 18 21 8 2018)
                                   '(0 20 21 21 8 2018))))
;; (plot (list (points   (map vector xs ys))
;;             (function (poly (fit xs ys 2)))))
