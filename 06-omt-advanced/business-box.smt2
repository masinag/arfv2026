(set-option :produce-models true)
(set-option :opt.priority box)

(define-const media-cost Int 2000)
(define-const media-customers Int 2)
(define-const media-rating Int 1)
(define-const media-hours Int 1)
(define-const appear-cost Int 500)
(define-const appear-customers Int 2)
(define-const appear-rating Int 5)
(define-const appear-hours Int 2)

(declare-const media-n Int)
(declare-const appear-n Int)

(define-const total-cost Int (+
  (* appear-cost appear-n)
  (* media-cost media-n)
))
(define-const total-customers Int (+
  (* appear-customers appear-n)
  (* media-customers media-n)
))
(define-const total-rating Int (+
  (* appear-rating appear-n)
  (* media-rating media-n)
))
(define-const total-hours Int (+
  (* appear-hours appear-n)
  (* media-hours media-n)
))

(assert (>= media-n 0))
(assert (>= appear-n 0))

(assert (>= total-customers 16))
(assert (>= total-rating 28))

(minimize total-cost)
(minimize total-hours)

(check-sat)
(get-objectives)
(load-objective-model 0)
(get-model)
(load-objective-model 1)
(get-model)
