(require "cl-csv")
(defparameter data (cl-csv:read-csv #P"dataHistory6.csv"))
(defparameter data_list ())
(defparameter time_values ())
(defparameter time_numbers ())
(defparameter points_values ())
(defparameter points_numbers ())
(defparameter time_mean 0)
(defparameter points_mean 0)
(defparameter points_dispersion 0)
(defparameter time_dispersion 0)

(loop for a in data
   do (if (string-equal (NTH 0 a) "ExpectimaxAgent")
             (push a data_list)))

(loop for a in data_list
   do (push (NTH 2 a) time_values))

(loop for a in data_list
   do (push (NTH 3 a) points_values))

(loop for a in time_values
   do (push (NTH 0 (with-input-from-string (in a)
  (loop for x = (read in nil nil) while x collect x))) time_numbers))

(loop for a in points_values
   do (push (NTH 0 (with-input-from-string (in a)
  (loop for x = (read in nil nil) while x collect x))) points_numbers))

(setq time_mean (/ (apply '+ time_numbers) (float(length time_numbers))))

(setq points_mean (/ (apply '+ points_numbers) (float(length points_numbers))))

(setq points_dispersion (/ (apply '+ (mapcar (lambda (x) (* x x)) (mapcar (lambda (n) (- n points_mean))
        points_numbers))) (length points_numbers)))

time_mean

points_mean

points_dispersion
