
clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

ifeq (serve,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "serve"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

export FLASK_ENV=dev
export FLASK_APP=planet/commands.py
export FLASK_DEBUG=1
serve: 
	flask $(RUN_ARGS)

admin-serve:
	@npm run dev --prefix admin

admin-build:
	@npm run build --prefix admin

dev:
	@$(MAKE) serve admin-serve -j 2