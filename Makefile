
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

export FLASK_ENV=dev
export FLASK_APP=planet/commands.py
export FLASK_DEBUG=1
server: 
	flask $(RUN_ARGS)

admin-serve:
	@npm run dev --prefix admin

admin-build:
	@npm run build --prefix admin

dev:
	@$(MAKE) server admin-serve -j 2