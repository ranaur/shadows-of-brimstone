dir := $(shell date +%Y%m%d%H%M%S)

all: 
	echo make all disabled for sdafety

reallyall: generatesvg generatepng generatepdf

backup:
	mkdir -p bak/$(dir)
	cp -R SVG PNG PDF bak/$(dir)

clear: clearsvg clearpng

clearsvg:
	rm -R SVG

clearpng:
	rm -R PNG

generatesvg:
	scripts/generate-svg

generatepng:
	scripts/generate-png

generatepdf:
	scripts/generate-pdf

abilitycards: usmarshall saloongirl bandido gunslinger

usmarshall: traveler resolve honor bountyhunting
saloongirl: fighting moxie acrobatics charm 
bandido: guns explosives brawling scoundrel
gunslinger: shootin showmanship wayofthegun reputation
acrobatics: Acrobatics-1.svg Acrobatics-2.svg Acrobatics-3.svg Acrobatics-4.svg
bountyhunting: "Bounty Hunting-1.svg" "Bounty Hunting-2.svg" "Bounty Hunting-3.svg" "Bounty Hunting-4.svg"
brawling: Brawling-1.svg Brawling-2.svg Brawling-3.svg Brawling-4.svg
charm: Charm-1.svg Charm-2.svg Charm-3.svg Charm-4.svg
explosives: Explosives-1.svg Explosives-2.svg Explosives-3.svg Explosives-4.svg
fighting: Fighting-1.svg Fighting-2.svg Fighting-3.svg Fighting-4.svg
guns: Guns-1.svg Guns-2.svg Guns-3.svg Guns-4.svg
honor: Honor-1.svg Honor-2.svg Honor-3.svg Honor-4.svg
moxie: Moxie-1.svg Moxie-2.svg Moxie-3.svg Moxie-4.svg
reputaion: Reputation-1.svg Reputation-2.svg Reputation-3.svg Reputation-4.svg
resolve: Resolve-1.svg Resolve-2.svg Resolve-3.svg Resolve-4.svg
scoundrel: Scoundrel-1.svg Scoundrel-2.svg Scoundrel-3.svg Scoundrel-4.svg
shooting: Shootin’-1.svg Shootin’-2.svg Shootin’-3.svg Shootin’-4.svg
showmanship: Showmanship-1.svg Showmanship-2.svg Showmanship-3.svg Showmanship-4.svg
traveler: Traveler-1.svg Traveler-2.svg Traveler-3.svg Traveler-4.svg
wayofthegun: Way Of The Gun-1.svg Way Of The Gun-2.svg Way Of The Gun-3.svg Way Of The Gun-4.svg
