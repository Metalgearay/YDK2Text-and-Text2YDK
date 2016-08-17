from collections import Counter
import sqlite3
import sys
deckname=sys.argv[1]
outputfile=sys.argv[2]
alist = [line.rstrip() for line in open(deckname)]
maindec=alist[alist.index("#main")+1:alist.index("#extra")]
extradec=alist[alist.index("#extra")+1:alist.index("!side")]
sidedec=alist[alist.index("!side")+1:]
maindecz=Counter(maindec)
extradecz=Counter(extradec)
sidedecz=Counter(sidedec)

f=open(outputfile,"w")
f.write("Main Deck:\n")
f.write("\n")
conn = sqlite3.connect('cards.cdb')
cur = conn.cursor()
conn2 = sqlite3.connect('official.cdb')
cur2 = conn2.cursor()
for keys in maindecz:	
	ids=(keys,)
	cur.execute("SELECT name FROM texts WHERE id=?",ids)
	temp=cur.fetchone()
	if temp is not None:
		f.write(str(temp[0])+" x "+str(maindecz[keys])+"\n")
	else:
		cur2.execute("SELECT name FROM texts WHERE id=?",ids)
		result=cur2.fetchone()
		f.write(str(result[0])+" x "+str(maindecz[keys])+"\n")
f.write("\n")
f.write("Extra Deck:\n")
f.write("\n")
for keys in extradecz:	
	ids=(keys,)
	cur.execute("SELECT name FROM texts WHERE id=?",ids)
	temp=cur.fetchone()
	if temp is not None:
		f.write(str(temp[0])+" x "+str(extradecz[keys])+"\n")
	else:
		cur2.execute("SELECT name FROM texts WHERE id=?",ids)
		result=cur2.fetchone()
		f.write(str(result[0])+" x "+str(extradecz[keys])+"\n")
f.write("\n")
f.write("Side Deck:\n")
f.write("\n")
for keys in sidedecz:	
	ids=(keys,)
	cur.execute("SELECT name FROM texts WHERE id=?",ids)
	temp=cur.fetchone()
	if temp is not None:
		f.write(str(temp[0])+" x "+str(sidedecz[keys])+"\n")
	else:
		cur2.execute("SELECT name FROM texts WHERE id=?",ids)
		result=cur2.fetchone()
		f.write(str(result[0])+" x "+str(sidedecz[keys])+"\n")
f.close()