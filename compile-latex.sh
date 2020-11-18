fileprefix="log_file"
latexfile="$fileprefix.tex"
indexfile="$fileprefix.idx"
pdflatex $latexfile
pdflatex $latexfile
makeindex $indexfile
pdflatex $latexfile
