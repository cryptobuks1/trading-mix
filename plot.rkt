#lang racket

(require plot/pict)
(require "poly-matrix.rkt")

(provide plot-with-x-as-time)

(define (plot-with-x-as-time xy)
  (parameterize ([plot-x-ticks (time-ticks)])
    (plot (points xy))))
