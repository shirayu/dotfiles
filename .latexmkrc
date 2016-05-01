#http://konn-san.com/prog/why-not-latexmk.html
$latex = 'platex -synctex=1 -halt-on-error';
$latex_silent     = 'platex -synctex=1 -halt-on-error -interaction=batchmode';
$bibtex           = 'pbibtex';
$dvipdf           = 'dvipdfmx %O -o %D %S';
$makeindex        = 'mendex %O -o %D %S';
$max_repeat       = 5;
$pdf_mode     = 3; # generates pdf via dvipdfmx

$pdf_previewer = "start evince";
$pdf_update_method = 0;
