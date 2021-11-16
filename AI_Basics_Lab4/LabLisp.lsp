(require "cl-csv")
(setq elems (cl-csv:read-csv #P"dataHistory.csv"))

(setq ExpectimaxAgent_list ())
(setq alphaBetaAgent_list ())


(loop for a in elems
   do (if (string-equal (NTH 0 a) "ExpectimaxAgent")
             (push a ExpectimaxAgent_list)))
(loop for a in elems
   do (if (string-equal (NTH 0 a) "AlphaBetaAgent")
             (push a alphaBetaAgent_list)))



(with-open-file (stream "ExpectimaxAgent.csv"
                     :direction :output
                     :if-exists :supersede
                     :if-does-not-exist :create)
                     (cl-csv:write-csv ExpectimaxAgent_list :stream stream))

(with-open-file (stream "AlphaBetaAgent"
                     :direction :output
                     :if-exists :supersede
                     :if-does-not-exist :create)
                     (cl-csv:write-csv alphaBetaAgent_list :stream stream))

