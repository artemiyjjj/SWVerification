#!/usr/bin/env bash

OUT="data/summary.csv"
echo "N,M,K,POLICY,LTLSPEC_OK,CTLSPEC_OK" > $OUT

for N in 1 2 3; do
  for M in 2 3 4 5; do
    for K in 2 3 4 5 6; do
      for POL in 0 1; do
        nuXmv \
		   -i model/client.smv \
		   -i model/window.smv \
		   -i model/env.smv \
		   -i model/main.smv \
		   -source <(cat <<EOF
set N $N
set M $M
set K $K
set POLICY $POL
reset
check_ltlspec -a
check_ctlspec -a
print_counterexample
EOF
) > tmp.log 2>&1

        LTL_OK=$(grep -c "false" tmp.log || true)
        CTL_OK=$(grep -c "false" tmp.log || true)
        if [ $LTL_OK -eq 0 ] && [ $CTL_OK -eq 0 ]; then
          LTL_RES=1; CTL_RES=1
        else
          LTL_RES=0; CTL_RES=0
        fi
        echo "$N,$M,$K,$POL,$LTL_RES,$CTL_RES" >> $OUT
      done
    done
  done
done

rm -f tmp.log