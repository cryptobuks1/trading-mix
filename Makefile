.PHONY: create-sqlite
create-sqlite:
	cd data;find . -name "ohlc-*" -exec jq -r '.["result"]|.["XXMRZEUR"][]|@csv' {} \; > alldata.csv

notebook:
	pipenv run jupyter notebook

test-mark-fixture:
test-mark-notify:
test-mark-newpeak:
test-mark-event:
test-mark-peakdiff:
test-mark-profit:
test-make-profit_persist:
test-mark-strategyhelper:
test-mark-%:
	pipenv run pytest -m $(*)

regression-test: test-mark-regression
