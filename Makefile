test:
	python setup.py test

.PHONY: test-mark-%
test-mark-%:
	tox -- -m $(*)
