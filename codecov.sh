#!/bin/bash

#############################################################################
# This script is what will run in CI (Continuous Integration) to get and    #
# upload code coverage data to `codecov.io` if we're running coverage       # 
# checks (Assumes code was build with coverage info for gcov)               #
#############################################################################

if [ "$RUN_COVERAGE" == "true" ]; then
    echo "Attempting to find and upload coverage reports"
    # `codecov.io` conveniently provides a script to automatically find
    # and upload coverage reports generated by gcov during the build process
    bash <(curl -s https://codecov.io/bash)
else 
    echo "Not running coverage, so did nothing"
fi
# The flags that we should use to build the code with coverage reporting enabled