#!/bin/bash

sphinx-apidoc -f -P -o docs_source/ $1
# sphinx-apidoc -F -f -P -o docs_source/ $1 # for initial docs
cd docs_source
make github