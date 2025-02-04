#!/bin/bash -e

GO_TEMPLATE_BINARY="./tests/gotemplate/gotemplate"

function build_go_template(){
    go build -o "${GO_TEMPLATE_BINARY}" ./tests/gotemplate/main.go
}

function run_tests(){
    pytest -svv \
        --log-cli-level=${LOG_LEVEL} \
        --log-cli-date-format="%Y-%m-%d %H:%M:%S%z" \
        --log-cli-format="%(asctime)s,%(msecs)03d %(levelname)-7s [%(name)s] %(message)s (%(module)s:%(lineno)d)"
}

function clean(){
    rm -f "${GO_TEMPLATE_BINARY}"
}

build_go_template
run_tests
