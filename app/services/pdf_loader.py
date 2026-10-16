import pymupdf

def extract(file):
    doc = pymupdf.open(file)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text

text = extract("data/Building Effective AI Agents.pdf")
words = text.split()
for start in range(0, len(words), 3):
    stop = start + 3
    chunk = words[start:stop]
    print(chunk)
