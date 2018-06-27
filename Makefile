
test-service:
	nosetests tests.service

test-unit:
	nosetests tests.unit

.PHONY: test-service test-unit
