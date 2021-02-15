import csv

keywords = []

with open('EnglishKeywords.txt','r',encoding='utf-8', newline='') as my_file:
	file_reader = csv.reader(my_file, delimiter=' ')
	for raw in file_reader:
		if 'sale' in set(raw):
			keywords.append(raw)

with open('sale.csv','w',encoding='utf-8', newline='') as file2:
	file_writer = csv.writer(file2, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
	for line_data in keywords:
		file_writer.writerow(line_data)