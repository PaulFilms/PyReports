# PyReports
Toolkit for Documentation and Reporting [ALPHA VERSION]

![Last commit](https://img.shields.io/github/last-commit/PaulFilms/PyReports?label=Último%20commit)


## Tools included
- Report Spreadsheets .xlsx Files
- Report .PDF Files


## 🔧 Installation

- Last released version

   ```plaintext
   Not available
   ```

- Latest development version

   ```plaintext
   pip install git+https://github.com/PaulFilms/PyReports.git@main
   ```


## 🧪Examples

### .XLSX

...


### .PDF

```python
from pyreports.pdf import PDFREPORT, colors, fontTypes

my_pdf = PDFREPORT(
    filePath=f'my_pdf_report.pdf',
    docTitle='TEST'
)

x = my_pdf.get_x()
y = my_pdf.get_y()

_, y = my_pdf.wr_header1(y, 'Hola mundo !')
_, y = my_pdf.wr_normal(y, 'Otro texto ...')
_, y = my_pdf.wr_normal(y, 'Otro texto 2 ...')

## Divider
_, y = my_pdf.wr_divider(y, 1)

## Centrado
_, y = my_pdf.wr_header1(y, '[ Hola mundo centrado ]', centered=True)
_, y = my_pdf.wr_normal(y, '[ Otro texto ... ]', centered=True)
_, y = my_pdf.wr_normal(y, '[ Otro texto 2 ... ]', centered=True)
_, y = my_pdf.wr_normal(y, '[ Otro texto mucho mas largooooooooo ]', centered=True)
_, y = my_pdf.wr_header1(y, '[ 2nd TITULO centrado diferenteeeee ]', centered=True)

## Divider
_, y = my_pdf.wr_divider(y, 1)
_, y = my_pdf.wr_divider(y, 1)
_, y = my_pdf.wr_normal(y, 'Otro texto ...')
# _, y = my_pdf.wr_normal(y, '❤️') # NO se pueden usar emoticonos como texto

## Free text
_, y = my_pdf.write(x=100, y=y-30, text='... TEXTO ROJO, Cursiva y Mas grande', font_name=fontTypes.italic_bold.name, font_size=18, color=colors.red)

## Imagen
img_path = r'data\my_img.png'
my_pdf.wr_image(
    x=my_pdf.get_x(True),
    y=my_pdf.get_y() - 10,
    img_path=img_path
)

my_pdf.showPage()
my_pdf.save()
```

## 📦 Dependencies

This project relies on the following open-source libraries:

| Package      | License       | Description                                                   |
|--------------|---------------|---------------------------------------------------------------|
| `pandas`     | BSD 3-Clause  | High-performance data manipulation and analysis.              |
| `openpyxl`   | MIT           | Read and write Excel `.xlsx` files.                           |
| `reportlab`  | BSD           | Dynamic PDF generation from Python.                           |
---


## TASK 📒

- re-define PDFREPORT and XLSREPORT with standards formats (normal, header 1 ... 3, caption, etc)
- PDF, re-define canvas size
- PDF, text size greater than the width of the canvas
- PDF, Create Tables and charts



## WARNINGS ⛔

- PDFREPORT its under construction yet
