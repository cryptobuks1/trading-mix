((python-mode . ((setq python-shell-interpreter "jupyter"
                       python-shell-interpreter-args "console --simple-prompt"
                       python-shell-prompt-detect-failure-warning nil)
                 (add-to-list 'python-shell-completion-native-disabled-interpreters
                              "jupyter")
                 (setenv "DATA_DIR" (concat (file-name-as-directory (projectile-project-root)) "data")))))
