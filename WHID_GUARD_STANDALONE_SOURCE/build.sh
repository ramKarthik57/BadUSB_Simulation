#!/bin/bash
set -e
echo '========================================================'
echo 'Compiling WHID-Guard 2027 IEEE Paper...'
echo '========================================================'
pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex
pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex
echo 'Done! Output generated: WHID_GUARD_2027.pdf'
