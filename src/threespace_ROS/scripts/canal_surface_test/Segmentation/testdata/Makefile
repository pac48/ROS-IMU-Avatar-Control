all: weight.dat

weight.dat: ~/Documents/Personal/weight/measure.db
	sqlite3 -header $< "select * from flatview" | tr "|" "\t" > $@
