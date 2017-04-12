
clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

ifeq (server,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "serve"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

server: 
	postflow $(RUN_ARGS)

serve:
	@$(MAKE) server run

admin-serve:
	@npm run dev --prefix admin

admin-build:
	@npm run build --prefix admin && rm -rf postflow/admin/static/* && cp -r admin/dist/* postflow/admin/static

dev:
	@$(MAKE) serve admin-serve -j 2

dependencies:
	pip install -r requirements.txt

install: dependencies
	clear
	postflow init
