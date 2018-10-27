(load-extension "./kraken" "scm_init_kraken_api_core_module")
(use-modules (ice-9 documentation))
(set! documentation-files (cons "doc" documentation-files))
(use-modules (kraken api core))
