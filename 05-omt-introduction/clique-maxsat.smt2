(set-option :produce-models true)

(declare-const A Bool)
(declare-const B Bool)
(declare-const C Bool)
(declare-const D Bool)
(define-fun at-most-one ((x Bool) (y Bool)) Bool
  (or (not x) (not y))
)

(assert (at-most-one B D))

(assert-soft (not A) :weight 1 :id clique-size)
(assert-soft (not B) :weight 1 :id clique-size)
(assert-soft (not C) :weight 1 :id clique-size)
(assert-soft (not D) :weight 1 :id clique-size)

(maximize clique-size)
(check-sat)
(get-model)
(get-objectives)

