(set-option :produce-models true)

(declare-const C1 Bool)
(declare-const C2 Bool)
(declare-const C3 Bool)
(declare-const C4 Bool)
(declare-const C5 Bool)
(declare-const C6 Bool)
(declare-const C7 Bool)
(declare-const C8 Bool)
(declare-const C9 Bool)
(declare-const C10 Bool)
(define-const A Bool true)
(define-const B Bool false)
(define-fun test-score
  ((A1 Bool) (A2 Bool) (A3 Bool) (A4 Bool) (A5 Bool)
   (A6 Bool) (A7 Bool) (A8 Bool) (A9 Bool) (A10 Bool))
  Int
  (+
    (ite (=  A1  C1) 10 0)
    (ite (=  A2  C2) 10 0)
    (ite (=  A3  C3) 10 0)
    (ite (=  A4  C4) 10 0)
    (ite (=  A5  C5) 10 0)
    (ite (=  A6  C6) 10 0)
    (ite (=  A7  C7) 10 0)
    (ite (=  A8  C8) 10 0)
    (ite (=  A9  C9) 10 0)
    (ite (= A10 C10) 10 0)
  )
)
(define-const john Int (test-score B B A A A B B A A A))

(assert (= 70 (test-score B B A B A B B A B B)))
(assert (= 50 (test-score B A A A B A B A A A)))
(assert (= 30 (test-score B A A A B B B A B A)))

(check-sat)
(get-model)
(get-value (john))


