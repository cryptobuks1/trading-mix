#lang racket
(require data-frame)

(provide fit-function)

(define (fit-function curve-data)
  (define xs (map (lambda (row)
                    (* 1.0 (vector-ref row 0)))
                  curve-data))

  (define ys (map (lambda (row)
                    (* 1.0 (vector-ref row 1)))
                  curve-data))

  (define df (make-data-frame))

  (define dxs (make-series "xs" #:data (apply vector xs)))
  (define dys (make-series "ys" #:data (apply vector ys)))

  (df-add-series df dxs)
  (df-add-series df dys)

  (df-least-squares-fit df "xs" "ys"
                        #:mode 'polynomial
                        #:polynomial-degree 3))
