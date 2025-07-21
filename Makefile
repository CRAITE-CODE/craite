.PHONY: all build test clean install publish

all: install build

install:
	@echo "Installing dependencies..."
	npm install
	cd sdks/python && pip install -r requirements.txt
	cd sdks/rust && cargo fetch
	cd sdks/go && go mod download

build:
	@echo "Building all packages..."
	npx lerna run build
	cd sdks/python && python setup.py build
	cd sdks/rust && cargo build --release --features cli
	cd sdks/go && go build -o bin/craite ./cmd/craite

test:
	@echo "Running tests..."
	npm test
	cd sdks/python && pytest
	cd sdks/rust && cargo test
	cd sdks/go && go test ./...

publish-npm:
	npx lerna publish

publish-pypi:
	cd sdks/python && python setup.py sdist bdist_wheel && twine upload dist/*

publish-crates:
	cd sdks/rust && cargo publish

clean:
	rm -rf node_modules packages/*/node_modules packages/*/dist
	rm -rf sdks/python/build sdks/python/dist sdks/python/*.egg-info
	rm -rf sdks/rust/target
	rm -rf sdks/go/bin
