
clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

server-dev:
	@./dev_site.sh runserver

admin-dev:
	@npm run dev --prefix admin

client-dev:
	@npm run dev --prefix client

dev:
	@$(MAKE) server-dev client-dev admin-dev -j 3