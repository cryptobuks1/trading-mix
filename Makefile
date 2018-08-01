.PHONY: create-sqlite
create-sqlite:
	cd data;find . -name "ohlc-*" -exec jq -r '.["result"]|.["XXMRZEUR"][]|@csv' {} \; > alldata.csv

test-mark-fixture:
test-mark-notify:
test-mark-newpeak:
test-mark-event:
test-mark-%:
	pipenv run pytest -m $(*)

regression-test: test-mark-regression
