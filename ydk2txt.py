from collections import Counter
import urllib, json
import sqlite3
import sys


totalsum=0
def get_price(name):
	url="http://yugiohprices.com/api/get_card_prices/"
	url=url+str(name)
	res=urllib.urlopen(url)
	content=json.load(res)
	if content['status'] != "fail": 
		print_tag=content['data'][0]['print_tag']
		price=float(content['data'][0]['price_data']['data']['prices']['low'])
		return (print_tag,price,)
	else:
		print("Could not find "+name)
		return None

def openDatabase():
	conn = sqlite3.connect('cards.cdb')
	cur = conn.cursor()
	return cur

def createDeckLists(deckname):
	alist = [line.rstrip() for line in open(deckname)]
	maindec=alist[alist.index("#main")+1:alist.index("#extra")]
	extradec=alist[alist.index("#extra")+1:alist.index("!side")]
	sidedec=alist[alist.index("!side")+1:]
	maindecz=Counter(maindec)
	extradecz=Counter(extradec)
	sidedecz=Counter(sidedec)
	return (maindecz,extradecz,sidedecz)

def searchForName(database,id):
	database.execute("SELECT name FROM texts WHERE id=?",id)
	result=database.fetchone()
	if result is not None:
		return result
	else:
		("Could not find %s please check if you have update data base" % id,)

def searchForCatagory(database,idx):
	ids=(idx,)
	database.execute("SELECT type FROM datas WHERE id=?",ids)
	result=database.fetchone()
	if result is not None:
		return result
	else:
		("Could not find %s please check if you have update data base" % id,)
def isMonster(category):
	if (category & 1 ) > 0:
		return True
	else:
		return False
def isSpell(category):
	if (category & 2 ) > 0:
		return True
	else:
		return False
def isTrap(category):
	if (category & 4) > 0:
		return True
	else:
		return False



def writeToFile(database,string,deck,mainFile,pricerpt,pricefl):
	mainFile.write("\n%s\n\n" % string)
	sums=0
	if pricerpt == "y":
		try:
			pricefl.write("%s:\n\n" % string)
		except:

			print ("Error reading file")
	for key in deck:
		search=(key,)
		name=searchForName(database,search)
		mainFile.write("%s x %s\n" % (name[0],deck[key]))
		if pricerpt == "y":
			tup=get_price(name[0])
			if tup is not None:
					print_tag=str(tup[0])
					price=str(tup[1]*deck[key])
					pricefl.write("\n%s - %s x %s $%s USD \n" % (name[0],print_tag,deck[key],price))
					sums+=float(price)
			else:
				pricefl.write("%s - Could not find price\n"% name[0])
	if pricerpt == "y":
		try:
			pricefl.write("\n%s Total : $%s USD \n\n" % (string,sums))
			global totalsum
			totalsum+=sums
		except:
			print ("Error reading file")
def mainDeckBreakDown(database,maindeck):
	monsterList={}
	spellList={}
	trapList={}
	unknown={}
	for key in maindeck:
		result=searchForCatagory(database,key)[0]
		if result is not None:
			if isMonster(result):
				monsterList[key]=maindeck[key]
			if isSpell(result):
				spellList[key]=maindeck[key]
			if isTrap(result):
				trapList[key]=maindeck[key]
			
		else:
			unknown[key]=maindeck[key]
	return (monsterList,spellList,trapList,unknown,)

def main():
	deckname=sys.argv[1]
	outputfile=sys.argv[2]
	filetowrite=open(outputfile,'w')
	pricefl=None
	answer=raw_input("Would you like to generate a price report(y/n)\n?")
	if answer == 'y':
		filename=raw_input("Please enter name you would like for the price report\n")
		pricefl=open("%s.txt" % filename,'w')
	decks=createDeckLists(deckname)
	maindeck=decks[0]
	extradeck=decks[1]
	sidedeck=decks[2]
	database=openDatabase()
	result=mainDeckBreakDown(database,maindeck)
	writeToFile(database,"Monsters (%d)" % sum(result[0].values()),result[0],filetowrite,answer,pricefl)
	writeToFile(database,"Spells (%d)" % sum(result[1].values()),result[1],filetowrite,answer,pricefl)
	writeToFile(database,"Traps (%d)"% sum(result[2].values()),result[2],filetowrite,answer,pricefl)
	writeToFile(database,"Extra Deck (%d)" % sum(extradeck.values()),extradeck,filetowrite,answer,pricefl)
	writeToFile(database,"Side Deck (%d)" % sum(sidedeck.values()),sidedeck,filetowrite,answer,pricefl)
	if len(result[3]) != 0:
		writeToFile(database,"Unkown Please Move",result[3],filetowrite,answer,pricefl)
	filetowrite.close()
	if answer == 'y':
		try:
			global totalsum
			pricefl.write("Deck total: $%s USD" % totalsum)
			pricefl.close()
		except:
			print("Error")
			pricefl.close()
			
if __name__ == "__main__":
	main()



