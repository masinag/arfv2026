(set-option :produce-models true)
; Bands:
; B - The Beagles
; A - AC/DC++
; R - Rolling Stonks
; K - Kanji West
;
; Slots:
; a - 18-19
; b - 19-20
; c - 20-21
; d - 21-22
; e - 22-23
; f - 23-24
(declare-const Ba Bool)
(declare-const Bb Bool)
(declare-const Bc Bool)
(declare-const Bd Bool)
(declare-const Be Bool)
(declare-const Bf Bool)
(declare-const Aa Bool)
(declare-const Ab Bool)
(declare-const Ac Bool)
(declare-const Ad Bool)
(declare-const Ae Bool)
(declare-const Af Bool)
(declare-const Ra Bool)
(declare-const Rb Bool)
(declare-const Rc Bool)
(declare-const Rd Bool)
(declare-const Re Bool)
(declare-const Rf Bool)
(declare-const Ka Bool)
(declare-const Kb Bool)
(declare-const Kc Bool)
(declare-const Kd Bool)
(declare-const Ke Bool)
(declare-const Kf Bool)
; The Beagles: from 19.00 to 21.00 or from 22.00 to 24.00
(define-const beagles Bool (or (and Bb Bc) (and Be Bf)))

; AC/DC++: 3 consecutive hours, no matter when.
(define-const acdcpp Bool (or
  (and Aa Ab Ac)
  (and Ab Ac Ad)
  (and Ac Ad Ae)
  (and Ad Ae Af)
))

; Rolling Stonks: from 18.00 to 19.00 or from 23.00 to 24.00
(define-const rollings Bool (or Ra Rf))

; Kanji West: 1 hour among all the slots, excluding the first slot and the last one.
(define-const kanjiw Bool (or Kb Kc Kd Ke))

; Slot a can be booked by at most one band
(assert (=> Ba (not (or Aa Ra Ka))))
(assert (=> Aa (not (or Ba Ra Ka))))
(assert (=> Ra (not (or Aa Ba Ka))))
(assert (=> Ka (not (or Aa Ba Ra))))
; Slot b can be booked by at most one band
(assert (=> Bb (not (or Ab Rb Kb))))
(assert (=> Ab (not (or Bb Rb Kb))))
(assert (=> Rb (not (or Ab Bb Kb))))
(assert (=> Kb (not (or Ab Bb Rb))))
; Slot c can be booked by at most one band
(assert (=> Bc (not (or Ac Rc Kc))))
(assert (=> Ac (not (or Bc Rc Kc))))
(assert (=> Rc (not (or Ac Bc Kc))))
(assert (=> Kc (not (or Ac Bc Rc))))
; Slot d can be booked by at most one band
(assert (=> Bd (not (or Ad Rd Kd))))
(assert (=> Ad (not (or Bd Rd Kd))))
(assert (=> Rd (not (or Ad Bd Kd))))
(assert (=> Kd (not (or Ad Bd Rd))))
; Slot e can be booked by at most one band
(assert (=> Be (not (or Ae Re Ke))))
(assert (=> Ae (not (or Be Re Ke))))
(assert (=> Re (not (or Ae Be Ke))))
(assert (=> Ke (not (or Ae Be Re))))
; Slot f can be booked by at most one band
(assert (=> Bf (not (or Af Rf Kf))))
(assert (=> Af (not (or Bf Rf Kf))))
(assert (=> Rf (not (or Af Bf Kf))))
(assert (=> Kf (not (or Af Bf Rf))))


(assert-soft beagles :weight 1 :id band-penalty)
(assert acdcpp)
(assert-soft rollings :weight 1 :id band-penalty)
(assert-soft kanjiw :weight 1 :id band-penalty)

(minimize band-penalty)

(check-sat)
(get-objectives)
(get-value (beagles acdcpp rollings kanjiw))
