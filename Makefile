test:
	nosetests
bootstrap:
	virtualenv ./venv
	$(SHELL) -c "source ./venv/bin/activate && pip install -r ./requirements.txt"
	echo "Your virtualenv is ready, type 'source ./venv/bin/activate' to use it"
