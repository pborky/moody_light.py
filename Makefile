
.PHONY : rmenv  updateenv  updatetestenv updatedevenv

initenv:
	virtualenv .
	bin/pip install -r requirements/base.txt
	echo '# Environment initialization placeholder. Do not delete. Use "make rmenv" to remove environment.' > $@

rmenv:
	rm -fr bin lib include local initenv src share ghost build


updateenv: initenv
	find . -name '*.pyc' -exec rm '{}' ';'
	bin/pip install -r requirements/base.txt

updatetestenv: updateenv
	bin/pip install -r requirements/test.txt

updatedevenv: updateenv
	bin/pip install -r requirements/dev.txt

