(set-option :produce-models true)

(declare-const x11 Real)
(declare-const x12 Real)
(declare-const x13 Real)
(declare-const x21 Real)
(declare-const x22 Real)
(declare-const x23 Real)
(declare-const x31 Real)
(declare-const x32 Real)
(declare-const x33 Real)
(define-fun red () Real 2)
(define-fun orange () Real 7)
(define-fun yellow () Real 3)
(define-fun is-tile ((cell Real)) Bool (or (= cell red) (= cell orange) (= cell yellow))))

(assert (is-tile x11))
(assert (is-tile x12))
(assert (is-tile x13))
(assert (is-tile x21))
(assert (is-tile x22))
(assert (is-tile x23))
(assert (is-tile x31))
(assert (is-tile x32))
(assert (is-tile x33))

; each row contains exactly one cell of each type
(assert (distinct x11 x12 x13))
(assert (distinct x21 x22 x23))
(assert (distinct x31 x32 x33))

; each col contains exactly one cell of each type
(assert (distinct x11 x21 x31))
(assert (distinct x12 x22 x32))
(assert (distinct x13 x23 x33))

(assert (= x13 orange))
(assert (= 12 (+ x11 x21 x31)))
(assert (= 42 (* x12 x22 x23)))
(assert (=  5 (+ x32 x33)))

(assert (> x21 x11))

(check-sat)
(get-model)
