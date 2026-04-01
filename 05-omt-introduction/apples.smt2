(set-option :produce-models true)

(declare-const n Int)
(define-fun tot_trees () Int (+ 50 n))
(define-fun apple_per_tree () Int (- 800 (* 10 n)))

(maximize (* tot_trees apple_per_tree))
(check-sat)
(get-objectives)
(get-model)
(exit)
