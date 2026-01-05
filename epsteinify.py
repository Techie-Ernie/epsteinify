import os
import fitz
import random
import argparse

parser = argparse.ArgumentParser(prog='Epsteinify', description="Turn your PDFs into the Epstein files")
parser.add_argument('-f,', '--filename')
parser.add_argument('-i', '--images', default="images/")
parser.add_argument('-r', '--redact', default=10)
args = parser.parse_args()

input_file = args.filename
pdfDoc = fitz.open(input_file)
num_pages = pdfDoc.page_count
for i in range(num_pages):
    page = pdfDoc[i]
    # redaction
    sentences = [s.strip() for s in page.get_text().split('.') if s.strip()]
    if not sentences:
        continue
    selected = random.choices(sentences, k=min(int(args.redact), len(sentences)))
    for sentence in selected:
        if not sentence:
            continue
        area = page.search_for(sentence)
        if not area:
            continue
        for a in area:
            page.add_redact_annot(a, text=" ", fill=(0,0,0))
    page.apply_redactions()
    
    # images
    img_list = page.get_images(full=True)
    if img_list:
      for img in img_list:
          xref = img[0]
          if args.images:
            choice = random.randint(1, len(os.listdir(args.images)))
            page.replace_image(xref, filename=f'{args.images}/epstein{choice}.jpg')


out_file = os.path.splitext(input_file)[0] + "_redacted.pdf"
pdfDoc.save(out_file)
print("Saved redacted PDF to", out_file)
