(set-option :produce-models true)

(declare-const A Int)
(declare-const B Int)
(declare-const C Int)
(declare-const D Int)
(define-fun pb ((x Int)) Bool (or (= x 0) (= x 1)))
(define-fun at-most-one ((x Int) (y Int)) Bool
  (<= (+ x y) 1)
)

(assert (pb A))
(assert (pb B))
(assert (pb C))
(assert (pb D))

(assert (at-most-one B D))

(maximize (+ A B C D))

(check-sat)
(get-model)
(get-objectives)

