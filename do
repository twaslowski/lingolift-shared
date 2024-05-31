#!/usr/bin/env bash


## formatting: Applies formatting
function task_format {
  poetry run isort .
  poetry run black .
}

## type-check: Runs mypy static type analysis
function task_type_check {
  poetry run mypy
}

## test: Runs unit tests
function task_test {
  poetry run coverage run -m pytest
}

function task_coverage() {
  task_test
  poetry run coverage html
  poetry run coverage xml -o test/coverage.xml
  poetry run coverage-badge -f -o test/coverage.svg
}


#-------- All task definitions go above this line --------#

function task_usage {
    echo "Usage: $0"
    sed -n 's/^##//p' <"$0" | column -t -s ':' |  sed -E $'s/^/\t/'
}

cmd=${1:-}
shift || true
resolved_command=$(echo "task_${cmd}" | sed 's/-/_/g')
if [[ "$(LC_ALL=C type -t "${resolved_command}")" == "function" ]]; then
    pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null
    ${resolved_command} "$@"
else
    task_usage
    if [ -n "${cmd}" ]; then
      echo "'$cmd' could not be resolved - please use one of the above tasks"
      exit 1
    fi
fi
