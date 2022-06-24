import pandas as pd
import pickle
import re
from timeis import tic, toc, timeis, yellow, line, green, white

print(f"{timeis()} {line}")
print(f"{timeis()} {yellow}5000 most common pāḷi words")
print(f"{timeis()} {line}")
tic()

print(f"{timeis()} {green}opening ebts csv", end=" ")

ebt_freq_df = pd.read_csv("../frequency maps/output/word count csvs/ebts.csv", header = None, index_col=None, sep="\t")
ebt_length = len(ebt_freq_df)

print(f"{white}{ebt_length}")

print(f"{timeis()} {green}opening dpd csv", end = " ")

dpd_df = pd.read_csv("../csvs/dpd-full.csv", index_col=None, sep="\t", dtype=str)
dpd_df.fillna("", inplace=True)

print(f"{white}{len(dpd_df)}")

anki5000_df = pd.DataFrame()

print(f"{timeis()} {green}inflections to headwords dict", end=" ")


with open("../inflection generator/output/inflection to headwords dict", "rb")as f:
	inflections = pickle.load(f)

print(f"{white}{len(inflections)}")

missing = open("output/missing.csv", "w")
missing.write(f"inflection\theadword\n")

counter = 0
used_headwords = []

print(f"{timeis()} {green}processing ebts")

for row in range(ebt_length): #ebt_length
	
	word = ebt_freq_df.iloc[row, 0]
	freq = ebt_freq_df.iloc[row, 1]

	if row %500 == 0:
		print(f"{timeis()} {counter}/5000\t{word}")

	try:

		headwords = inflections[word]["headwords"]
		
		for headword in headwords:
			if counter >= 5000:
				break
			elif counter < 5000 and \
			headword not in used_headwords:
				used_headwords.append(headword)
				test1 = dpd_df['Pāli1'] == headword
				test2 = dpd_df['Meaning IN CONTEXT'] != ""
				test3 = dpd_df['Source1'] != ""
				filter = test1 & test2 & test3
				dpd_row = dpd_df.loc[filter]

				if not dpd_row.empty:
					anki5000_df = anki5000_df.append([dpd_row])
					counter += 1

				else:
					if not re.findall(fr"\d", headword) or \
					re.findall("1", headword):
						missing.write(f"{word}\t{headword}\n")

	except: 
		# print(word, "does not exist in dpd")
		if counter >= 5000:
			break


print(f"{timeis()} {green}saving csv")
output_file = "output/anki5000.csv"

anki5000_df.reset_index(drop=True, inplace=True)
anki5000_df['GoogleForm'] = f"""Spot a mistake? <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSf9boBe7k5tCwq7LdWgBHHGIPVc4ROO5yjVDo1X5LDAxkmGWQ/viewform?usp=pp_url&entry.438735500=""" + anki5000_df.Pāli1 + """&entry.1433863141=Anki5000">Fix it here</a>."""

anki5000_df.to_csv(output_file, sep="\t", index = None, header=None)
missing.close()
toc()





