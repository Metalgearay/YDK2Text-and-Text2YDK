Here are two simple python scripts that handel conversion from a ydk file( used in devpro and ygopro) to a text and a text to a ydk file:

Setup:

You need to install at least python 2.7.x( NOTE YOU DO NEED PYTHON 2.7 BECAUSE OF RAW_INPUT WILL PORT AT A LATER POINT) from https://www.python.org/downloads/ for your platform


Other than that you are ready to go

Usage:

python ydk2txt xxx.ydk yyy.txt

xxx is source ydk file (needs to be in sample folder of the python scripts to work)
yyy is output file (created in the folder of the scripts)

python txt2ydk xxx.txt yyy.ydk

xxx is source txt file (needs to be in sample folder of the python scripts to work)
yyy is output file ydk (created in the folder of the scripts)

NOTE IT MUST BE IN THE SAME EXACT FORMAT OF THE SAMPLE BLACKWINGS TEXT FILE

Future plans:

Break up main deck in spells and traps and total up the scores
Add some more flexability for the source text file
