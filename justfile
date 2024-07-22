alias l := lock
alias i := install
alias d := develop
alias u := uninstall
alias c := clean

lock:
	uv pip freeze | uv pip compile - -o requirements.txt
install:
	uv pip install -e .
develop:
	uv pip install -e .[dev] && pre-commit install
uninstall:
	uv pip uninstall dixa-api-client
clean:
	rm -rf *.egg-info .ruff_cache
