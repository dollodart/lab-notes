# Motivation

There are several advantages to digital notes over paper notebooks:

- The text files are searchable
- The average typing speed is 32.5 wpm and the average handwriting speed is 13 wpm, a 2.5 times increase in the speed, which lowers the barrier for experimentalists to write more descriptive lab notes
- Data and their analysis may be preserved in spreadsheet files which can later be revisited and used in analytics
- Contents may be automatically compiled into printable documents having structure and cross-reference that is tedious to do by hand
- Analytics may be run to assist students and PIs in assessing long-term trends in chemical consumption, equipment maintenance, and other accounting tasks

These advantages of digital notebooks are shown here as a FOSS alternative to commercial notebooks.

# What the program does

Python scripts are used with fill out LaTeX templates to then compile
printable summaries of lab notes. Both the lab notes in dated
directories and the images and tables contained therein, as well as
summary sheets made by the laboratory worker, are put into an automatic
cross-referenced document. References and indexing are made by user
specification in the markdown file with LaTex commands (like \ref to
make links, with automatic labeling of sections, images, and tables in
the templates) and by user specifications in the compile file (to index
specific words).

Analytics on template based files for chemical consumption and
instrument calibration drift are given, and some utilities for searching
the files are also given.

# Details on what the program does

## Automatic Document Compilation

The program uses two experiment related directories. One is in
summaries, which are what the user prepares as descriptions of
experiments which range over some times, in a markup or spreadsheet
file. The other is in dated lab directories, which may contain
descriptive notes, images, data files acquired in that day, e-mail
records from facilities or business contacts, and whatever else may
be relevant. It iterates through all dated directories, and applies a
formatting for each file depending on its suffix to be included in the
document. The user must define the LaTex template and the programming to
handle whichever file format is desired. These are added to the LaTeX
document in order of date and within date by a prescribed order of
files.

### Latex Encoding of Unicode Equations

The writing of equations in lab notes is likely infrequent, but given
the mathematical typesetting purpose of TeX it would be silly not to
include a conversion. Conversion is simply accomplished by a dictionary
which replaces unicode with Latex commands. The difficulty would be in
having the program understand what delimiters for math mode there are.
But, the student can apply the own delimiters while using unicode, as in

$$ ε = (Θ - 1)^2 .$$

to enable simple dictionary substitution. That is assumed here.

The package pylatexenc is used, though note this only supports the 4
hex-digit greek letters, not the mathematical italic 5 hex-digit greek
letters. See their uni2latexmap file for a full listing.

## Automatic Inventory and Analytics on Templated Files

By using files following a template analytics can be done. Here
examples of time history of consumption of chemicals and of instrument
calibration drift are given. Other ideas may be to track maintenance
records, development of standard operating procedures, and so on.

Files in spreadsheets can conform to a template, while allowing the
user to have large amounts of freedom to put their own notes or other
calculations, by either indicating by color or enforcing by protection
that certain cells or other features are not to be edited, e.g., those
cells corresponding to column names and the sheet names.

# Supported file formats

The lab notes should be in Markdown format so that they may be formatted
with Pandoc into LaTex. Any other markup language would do and it is
obvious how to edit to support those.

The data summary files are either in a markup language like YAML or in a
spreadsheet data format (here xlsx, a type of binary-encoded xml which
is used by Microsoft Excel but is also an ISO standard data format). The
YAML file should be a list of dictionaries, in order to construct a
dataframe. Due to common use of spreadsheets, the examples given here
are mostly with them. Excel workbooks have some extra difficulties, like
in the read and write speeds, and preserving formatting on updates,
which are not yet fully addressed.

If a user wishes customized treatment of some files of that
type, say SEM images in a png format, they may invent the
relevant file suffix as in `SEM-sample-1213.png_sem`. This
can be registered to a default application in, for linux,
`/usr/share/applications/defaults.list`. Alternatively, if they wish it
to be treated as a standard item for document compiling but used for
accounting in other scripts, they can assign a prefix to it, such as
`ReagentTemplate` in `ReagentTemplate-alltagexp.xlsx`

# Table of Contents and Indexing

A table of contents is automatically generated from the user provided
subtitles, and each days lab notes are assigned a section with title of
the date. Index words may be specified in the compile file. The user can
also use the index syntax directly, like the ref syntax, in the markdown
body, e.g., in cross-referencing indexes.

## Semiautomatic Indexing

Given the fact that the digital files are searchable for keywords and
phrases, the value of a static index for print documents derived from it
is only for the case that the digital files are not available to all for
which the print files are made.

But if there is any interest, I did find a Bachelors honors thesis from
an M. Holler (see references).  The conclusion is you can get ~10%
agreement with a professionally written index using machine learning,
in particular naive Bayes classification, using a feature set derived
from Wikipedia article titles and label (make an index entry for) each
paragraph. It's possible another machine learning method might work
better as acknowledged by the author. One could also use a large set of
free textbooks and other materials for training and testing sets (in the
thesis, an OpenStax textbook *Biology* is used as the testing set).

## TODOs

- Use an excel writing package that allows values to be substituted
while preserving formatting when updating excel files
- Call excel VBA to export to csv and read csv with Python. This is the
fastest way to read excel files, even though there is an ISO standard
for the xlsx format. Difficult to develop outside a windows environment.
- Expose utilities through a CLI, also allow the date range to be
specified outside of the date iterator utility. This is because you
often want to search in date ranges not the same as the ones you compile
to.

Please raise an issue or e-mail me at davidollodart*at*gmail.com if you
have a suggestion or use case you would like developed.

# References

Automated Textbook Indexing with Naive Bayes Classifier Trained on Wikipedia Articles
M. Holler
