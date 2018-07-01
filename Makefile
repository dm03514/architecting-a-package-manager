
lint:
	pycodestyle .

test-unit:
	nosetests tests.unit

test-integration:
	nosetests tests.integration

test-service:
	nosetests tests.service

.PHONY: test-service test-unit lint test-integration
