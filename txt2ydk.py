import sqlite3
import sys
deckname=sys.argv[1]
outputfile=sys.argv[2]
f=open(outputfile,'w')
alist = [line.rstrip().rstrip('') for line in open(deckname)]
maindec=alist[alist.index("Main Deck:")+1:alist.index("Extra Deck:")]
maindec=filter(None,maindec)
extradec=alist[alist.index("Extra Deck:")+1:alist.index("Side Deck:")]
extradec=filter(None,extradec)
sidedec=alist[alist.index("Side Deck:")+1:]
sidedec=filter(None,sidedec)
f.write("#created by.. txt2ydk\n")
f.write("#main\n")

conn = sqlite3.connect('cards.cdb')
cur = conn.cursor()


for cardname in maindec:
	result=cardname.split(" x ")
	ids=(result[0],)
	i=int(result[1])
	cur.execute("SELECT id FROM texts WHERE name=?",ids)
	temp=cur.fetchone()
	if temp is not None:
		while i > 0:
			f.write(str(temp[0])+"\n")
			i-=1
	else:
		print ("Error could not find card "+result[0]+" skipping checking spelling or format")
f.write("#extra\n")
for cardname in extradec:
	result=cardname.split(" x ")
	ids=(result[0],)
	i=int(result[1])
	cur.execute("SELECT id FROM texts WHERE name=?",ids)
	temp=cur.fetchone()
	if temp is not None:
		while i > 0:
			f.write(str(temp[0])+"\n")
			i-=1
	else:
		print ("Error could not find card "+result[0]+" skipping checking spelling or format")
f.write("!side\n")
for cardname in sidedec:
	result=cardname.split(" x ")
	ids=(result[0],)
	i=int(result[1])
	cur.execute("SELECT id FROM texts WHERE name=?",ids)
	temp=cur.fetchone()
	if temp is not None:
		while i > 0:
			f.write(str(temp[0])+"\n")
			i-=1
	else:
		print ("Error could not find card "+result[0]+" skipping checking spelling or format")