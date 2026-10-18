import pymupdf

def extract(file):
    doc = pymupdf.open(file)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
    
# def chunk_text(text, chunk_size=3):
#     words = text.split()
#     chunks = []

#     for start in range(0, len(words), chunk_size):
#         stop = start + chunk_size
#         chunk = words[start:stop]
#         chunks.append(chunk)

#     return chunks
def chunk_text(text, chunk_size=100, overlap=20):
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        stop = start + chunk_size
        chunk = words[start:stop]
        chunks.append(" ".join(chunk))

    return chunks
text = extract("data/Building Effective AI Agents.pdf")
chunks = chunk_text(text)

print("Total words:", len(text.split()))
print("Total chunks:", len(chunks))
print("\nFirst chunk:\n", chunks[0])
print("\nSecond chunk:\n", chunks[1])
print("First chunk type:", type(chunks[0]))
print("First chunk words:", len(chunks[0].split()))
print("Last chunk words:", len(chunks[-1].split()))