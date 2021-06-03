#!/bin/bash

npm run build
mv dist/index.html osview/templates/workspace.html
rm -r dist
