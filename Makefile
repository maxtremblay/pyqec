test:
	poetry run maturin develop
	poetry run pytest

example:
	poetry run maturin develop
	for file in $$(ls -f examples/*.py) ; \
		do \
			poetry run python $$file; \
		done

