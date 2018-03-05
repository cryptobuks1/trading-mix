.PHONY: test
test:
	tox

.PHONY: test-mark-%
test-mark-%:
	tox -- -m $(*)
