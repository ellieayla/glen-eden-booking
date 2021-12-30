
.PHONY: runonce
runonce:
	scrapy crawl parkpassproject --loglevel=INFO

.PHONY: run
run:
	while [ 1 ]; do scrapy crawl parkpassproject --loglevel=WARNING; sleep 300; done

.PHONY: serve
serve:
	python -m http.server 8000

.PHONY: install
install:
	pip install -r requirements.txt
