(set-option :produce-models true)
(declare-const xa Int)
(declare-const xb Int)
(declare-const xc Int)
(define-const deliver-norm Int (+ (* xa 10) (* xb 15) (* xc 20)))
(define-const deliver-high Int (+ (* xa 21) (* xb 18) (* xc 15)))

(assert (and (>= xa 0) (>= xb 0) (>= xc 0)))
(assert (>= (+ xa xb xc) 100))

(minmax deliver-norm deliver-high)
(check-sat)
(get-objectives)
(get-model)
(get-value (deliver-norm deliver-high))

