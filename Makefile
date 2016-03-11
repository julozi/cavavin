NAME=cavavin
COVERDIR=cover_html

###################################################################
# Standard targets.
###################################################################
.PHONY : install4dev
install4dev:
	virtualenv env
	env/bin/pip install -r requirements.txt
	env/bin/pip install -r requirements-dev.txt
	cp app.development.cfg app.cfg

.PHONY : clean
clean:
	find . -name "*.pyc" -o -name "*​.pyo" | xargs -n1 rm -f
	rm -Rf build
	rm -rf $(COVERDIR)
	rm -Rf dist

.PHONY : tests
tests:
	env/bin/nosetests -v --with-progressive

.PHONY : coverage
coverage:
	rm -f .coverage
	rm -rf $(COVERDIR)
	env/bin/nosetests -v --with-progressive --with-coverage --cover-erase --cover-branches --cover-html --cover-html-dir=$(COVERDIR) --cover-package=$(NAME)

.PHONY : flake8
flake8:
	env/bin/flake8 $(NAME)
