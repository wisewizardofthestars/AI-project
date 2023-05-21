for test in src/*.txt; do
    python3 src/bimaru.py < $test;
done
