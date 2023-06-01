for x in instances-students/*.txt; do
    python3 src/bimaru.py < $x > ${x%.txt}.myout;

    diff -cB -w ${x%.txt}.out ${x%.txt}.myout > ${x%.txt}.diff ;
    if [ -s ${x%.txt}.diff ]; then
        failed=$((failed+1))
        echo -e "${RED} FAIL: $x. See file ${x%.txt}.diff ${NC}"
    else
        passed=$((passed+1))
        echo -e "${GREEN} PASS: $x ${NC}"
        rm -f ${x%.txt}.diff ${x%.txt}.myout ; 
    fi
done
