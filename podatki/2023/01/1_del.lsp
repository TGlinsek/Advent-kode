; common-lisp

(setq file-path "input.txt")

(defun read-file (file-path)
  (with-open-file (stream file-path :direction :input)
    (let ((contents (make-string (file-length stream))))
      (read-sequence contents stream)
      contents)))

(setq file-contents (read-file file-path))

#|
; koda, ki baje tudi deluje in ti že sproti vse da v en string:

(defun read-file-as-string (file-path)
  (with-open-file (stream file-path :direction :input)
    (let ((contents ""))
      (loop for line = (read-line stream nil)
            while line
            do (setq contents (concatenate 'string contents line "\n")))  ; namesto concatenate bi lahko tudi hranili v nov seznam
      contents)))

(setq file-contents (read-file-as-string file-path))
|#


#| 
(setq file-contents "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet")
|#

(defun obrni (sez) (
    if (equal (length sez) 0) 
        '() 
        (cons (first(last sez)) (obrni (butlast sez)))))  ; Zakaj ne smejo biti oklepaji okoli '()?

(setq sez '())  ; tu je lahko z apostrofom ali brez. Ne vem, zakaj.
(loop for i from 0 to (- (length file-contents) 1) 
    do (let ((crka (char file-contents i)))
        (
            if (equal crka #\Newline) 
                (setq sez  (append sez (list '())))
                (setq sez (append (butlast sez) (list (cons crka (first (last sez))))))
        )
    )
)
; (princ sez)

(setq sez2 '())
(loop for s in sez 
    do (setq sez2 (append sez2 (list (obrni s))))  ; pazi, to ni isto kot (obrni (list s)), for some reason
)

; (princ sez2)

(setq sez sez2)

(defun isdigit (crka) (case crka
    (#\1 t)
    (#\2 t)
    (#\3 t)
    (#\4 t)
    (#\5 t)
    (#\6 t)
    (#\7 t)
    (#\8 t)
    (#\9 t)
    (#\0 t)
    (otherwise nil)
    )
)

(defun vrednost (crka) (case crka
    (#\1 1)
    (#\2 2)
    (#\3 3)
    (#\4 4)
    (#\5 5)
    (#\6 6)
    (#\7 7)
    (#\8 8)
    (#\9 9)
    (#\0 0)
    (otherwise 7)
    )
)  ; zaka case ne deluje s stringi, samo s char?


(defvar stevec 0)
(defvar kontrola nil)
(defvar v 0)

(loop for podsez in sez
    do (progn 
        (setq kontrola nil) 
        ; loop za najdbo prve števke v vrstici
        (loop for crka in podsez 
            do (if (equal kontrola nil) 
                    (if (isdigit crka) 
                        ; prištejemo desetkratnik prve števke števcu
                        (progn (setq stevec (+ stevec (* 10  (vrednost crka)))) (setq kontrola t))  ; zaka je treba progn devat?
                        (progn)
                    ) 
                    (progn)
               )
        )
        ; loop za najdbo zadnje števke v vrstici
        (loop for crka1 in podsez 
            do (if (isdigit crka1) 
                    (setq v (vrednost crka1)) 
                    (progn)
                )                                      
        )
        (setq stevec (+ stevec v))  ; prištejemo zadnjo števko števcu
    )
)

(princ stevec)
