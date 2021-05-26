maturin develop
cd docs/api
make html
cd ../..
cp docs/api/build/html/* ../gh-pages/ -r


