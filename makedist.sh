ts=$(date +%s)
fn=MSDS-grader-$ts.zip
pushd grader && zip -r "$fn" . -x submission/* \*__pycache__\*
popd
mkdir -p dist
mv "grader/$fn" dist/
