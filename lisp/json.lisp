(ql:quickload 'yason)
(ql:quickload 'alexandria)
(defun load-ohlc (query)
  (with-open-file (stream "~/projects/kraken-bash/ohlc-1513226220.json")
    (loop for object = (read-line stream nil nil)
          while object
          collect (funcall query (yason:parse object)))))

(defun get-data (json)
  (gethash (string "XXMRZEUR")(gethash (string "result") json)))

;;; (first(first(load-ohlc #'get-data)))
