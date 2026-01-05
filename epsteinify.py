import os
import fitz
import random
import argparse

input_file = 'paper.pdf'
pdfDoc = fitz.open(input_file)
num_pages = pdfDoc.page_count
for i in range(num_pages):
    page = pdfDoc[i]
    # redaction
    sentences = [s.strip() for s in page.get_text().split('.') if s.strip()]
    if not sentences:
        continue
    selected = random.choices(sentences, k=min(10, len(sentences)))
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
          choice = random.randint(1, len(os.listdir('images/')))
          page.replace_image(xref, filename=f'images/epstein{choice}.jpg')


out_file = os.path.splitext(input_file)[0] + "_redacted.pdf"
pdfDoc.save(out_file)
print("Saved redacted PDF to", out_file)
