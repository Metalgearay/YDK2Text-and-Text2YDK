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
					pricefl.write("%s - %s x %s $%s USD \n" % (name[0],print_tag,deck[key],price))
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
	writeToFile(database,"Main Deck",maindeck,filetowrite,answer,pricefl)
	writeToFile(database,"Extra Deck",extradeck,filetowrite,answer,pricefl)
	writeToFile(database,"Side Deck",sidedeck,filetowrite,answer,pricefl)
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



