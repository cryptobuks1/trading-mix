(ql:quickload "yason")
(with-open-file (stream "~/projects/kraken-bash/ohlc-1513226220.json")
  (loop for object = (read-line stream nil nil)
        while object
        collect (yason:parse object)))
