PYTHON = python3

ALL  = $(INTRO) $(WARMUP) $(NORMAL) $(HARD)
SRC  = ${ALL:%=%.py}
SOL  = ${WARMUP:%=sol.%} ${WARMALT:%=alt.%} ${NORMAL:%=sol.%} ${HARD:%=sol.%}
WSOL = ${WARMUP:%=%.sol} $(WARMALT:%=%.alt)
WSRC = ${WSOL:%=%.py}
EX   = $(WARMUP) $(NORMAL) $(HARD)

CHECK_CMD = cmd() { $(PYTHON) $$1.py ; } ; banner=test
MYPY_CMD  = cmd() { sh ../util/mypy.sh $$@ ; } ; banner=mypy

CHECK  = printf "[$$banner] %-20s " "$$b" ; \
	 if cmd ./$$b > .check.out 2>&1 ; then ok=$$b ; else fail=$$b ; fi ; \
	 if test "$$ok" = $$b ; then echo ok ; else echo fail ; sed -e "s,^,  ," < .check.out ; fi

all: $(WSRC)
	@:

$(WSRC):
	@for b in $(WARMUP); do \
	    perl -p0777e 's,\n*import run_tests.*,,' sol.$$b.py > $$b.sol.py; \
	    touch -r sol.$$b.py $$b.sol.py; \
	done

check:
	@$(CHECK_CMD) ; for b in $(EX); do $(CHECK); done ; test -z "$$fail"

check-sol:
	@$(CHECK_CMD) ; for b in $(INTRO) $(SOL); do $(CHECK); done ; test -z "$$fail"

mypy-sol:
	@$(MYPY_CMD) ; for b in $(ALL); do $(CHECK); done ; test -z "$$fail"

clean:
	rm -f $(WSRC)
	rm -f *.core core *~ a.out .check.out $(CLEAN)
	if test -d __pycache__; then rm -r __pycache__; fi
	if test -d .mypy_cache; then rm -r .mypy_cache; fi

show:
	@echo ${$(var):%=$(prefix)%$(suffix)}

import: $(WSRC)
	$(MAKE) clean
	if test -f assignment.json -o -f lecture.json; then $(SUBJECT) import; fi

.PHONY: all check check-sol clean show import
