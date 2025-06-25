'''
Toolkit with simplified functions and methods for create .pdf Reports

⚠️INCOMPLETE
'''
__update__ = '2025.06.25'

import os
# from dataclasses import dataclass
from enum import Enum
from PIL import Image
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import pagesizes
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

## TOOLS
## _________________________________________________________________________________________________________________

''' ❕PAGE SIZE:
In ReportLab, the size of your Canvas (and all coordinates/dimensions you use) is expressed in points, 
where 1 point = 1/72 of an inch

from reportlab.lib.units import cm, inch

print(cm)    # ≈ 28.35 point
print(inch)  # 72 point
'''

# class orientations(Enum):
# 	landscape = 'landscape'
# 	portrait = 'portrait'

# class pase_sizes(Enum):
# 	'''
# 	Tuple[x, y]
# 	'''
# 	# A4_horizontal = (cm*21, cm*29.7) # 210 x 297 mm
# 	# A4_vertical = (cm*29.7, cm*21) # 297 x 210 mm
# 	A4_horizontal = pagesizes.landscape(pagesizes.A4) # 210 x 297 mm
# 	A4_vertical = pagesizes.portrait(pagesizes.A4) # 297 x 210 mm

class fontTypes(Enum):
	'''
	Registered Font Types in text format
	'''
	normal = TTFont('normal', 'arial.ttf')
	bold = TTFont('bold', 'arialbd.ttf')
	italic = TTFont('italic', 'ariali.ttf')
	italic_bold = TTFont('italic_bold', 'arialbi.ttf')

# @dataclass
# class richText():
# 	'''
# 	DataClass for defining the content and formatting of a text string
# 	'''
# 	value: str = ""
# 	font: fontTypes = fontTypes.normal
# 	size: float = 8
# 	color: colors = colors.black
		
class PDFREPORT:
	'''
	Un A-4 a 72 ppp    595 x 842
	Default Font: Arial
	'''
	def __init__(self, 
			filePath, ## path_file.pdf
			docTitle: str, 
			pagesize: tuple[float, float] = pagesizes.portrait(pagesizes.A4), ## Tuple[x: float, y: float]
			marginTop: float = cm*1, ## 1 cm
			marginBottom: float = cm*2, ## 1 cm
			marginLeft: float = cm*1.5, ## 1.5 cm
			marginRight: float = cm*1, ## 1 cm
		):
		
		self.PDF = canvas.Canvas(
			filePath,
			pagesize=pagesize
		)

		## DOCUMENT NAME
		if docTitle:
			self.PDF.setTitle(docTitle)
		# else:
		# 	self.PDF.setTitle("REPORT")
		
		## FONTS
		for f in fontTypes:
			pdfmetrics.registerFont(f.value)
		
		## PAGE SIZE / MARGINS
		self.spacing = 5
		# self.pageSize = pagesize
		self.marginTop = marginTop
		self.marginBottom = marginBottom
		self.marginLeft = marginLeft
		self.marginRight = marginRight

		## Get objects
		# lineWidth = self.PDF._lineWidth
		# print(lineWidth)
		# fillColor = self.PDF._fillColorObj
		# print(fillColor)

		## SAVING THE .PDF FILE
		# self.PDF.save()

		## Cursor Position
		# self.X: float = 0.0
		# self.Y: float = 0.0

	def showPage(self):
		self.PDF.showPage()

	def save(self):
		self.PDF.save()
	
	def get_x(self, centered: bool = False) -> float:
		if centered:
			return (( self.PDF._pagesize[0] - self.marginLeft - self.marginRight ) / 2 ) + self.marginLeft
		else:
			return self.marginLeft
	
	def get_y(self) -> float:
		return self.PDF._pagesize[1] - self.marginTop

	def wr_divider(self, y: float, line_width: float = 1.5) -> tuple[float, float]:
		self.PDF.setLineWidth(line_width)
		self.PDF.line(
			x1=self.marginLeft, 
			y1=y, 
			x2=self.PDF._pagesize[0] - self.marginRight, 
			y2=y
		)
		return self.get_x(), y - 20

	def wr_image(self, x: float, y: float, img_path: str, size_percent: float = 100) -> None:
		if not os.path.exists(img_path):
			return
		img = Image.open(img_path)
		
		if img.mode not in ("RGB", "RGBA"):
			img = img.convert("RGB")

		## Crea un buffer en memoria con formato PNG
		buf = BytesIO()
		img.save(buf, format="PNG")
		buf.seek(0)
		reader = ImageReader(buf)

		## dpi size
		dpi = img.info.get('dpi', (72, 72))
		w_px, h_px = img.size
		w_pt = w_px * (72 / dpi[0])
		h_pt = h_px * (72 / dpi[1])

		self.PDF.drawImage(
			reader, 
			x=x, 
			y=y-h_pt, 
			width= img.size[0] * size_percent/100, 
			height= img.size[1] * size_percent/100,
			mask='auto'
		)

	def write(self, 
		   x: float, y: float, text: str, 
		   font_name: str = fontTypes.normal.name,
		   font_size: float = 12,
		   color: colors = colors.black,
		   ):
		txt = self.PDF.beginText()
		txt.setTextOrigin(x, y)
		txt.setFont(font_name, font_size)
		txt.setLeading(font_size + self.spacing)
		txt.setFillColor(color)
		txt.textLine(text)
		
		self.PDF.drawText(txt)

		return txt.getX(), txt.getY()

	def wr_normal(self, y: float, text: str, centered: bool = False) -> tuple[float, float]:
		# font_name = fontTypes.normal.name
		# font_size = 12
		# self.PDF.setFont(font_name, font_size, leading=font_size + self.spacing)
		
		# x=self.get_x()
		# if centered:
		# 	text_width = self.PDF.stringWidth(text, self.PDF._fontname, self.PDF._fontsize)
		# 	x = self.get_x(centered=centered) - (text_width / 2)	

		# # Construye el TextObject
		# txt = self.PDF.beginText()
		# txt.setTextOrigin(x, y)
		# txt.setFont(font_name, font_size)
		# txt.setLeading(font_size + self.spacing)
		# txt.textLine(text)
		# self.PDF.drawText(txt)

		# # total_spacing = self.spacing + self.PDF._fontsize
		# return 0.0, txt.getY() # y - total_spacing

		font_name = fontTypes.normal.name
		font_size = 12

		x=self.get_x()
		if centered:
			text_width = self.PDF.stringWidth(text, font_name, font_size)
			x = self.get_x(centered=centered) - (text_width / 2)
		
		new_x, new_y = self.write(x, y, text, font_name, font_size)

		return new_x, new_y

	def wr_header1(self, y: float, text: str, centered: bool = False) -> tuple[float, float]:
		# font_name = fontTypes.bold.name
		# font_size = 14
		# self.PDF.setFont(font_name, font_size, leading=font_size + self.spacing)
		
		# x=self.get_x()
		# if centered:
		# 	text_width = self.PDF.stringWidth(text, self.PDF._fontname, self.PDF._fontsize)
		# 	x = self.get_x(centered=centered) - (text_width / 2)	

		# # Construye el TextObject
		# txt = self.PDF.beginText()
		# txt.setTextOrigin(x, y - self.spacing)
		# txt.setFont(font_name, font_size)
		# txt.setLeading(font_size + self.spacing)
		# txt.textLine(text)
		# self.PDF.drawText(txt)

		# # total_spacing = self.spacing + self.PDF._fontsize
		# return 0.0, txt.getY() # - self.spacing # y - total_spacing
		
		font_name = fontTypes.bold.name
		font_size = 14

		x=self.get_x()
		if centered:
			text_width = self.PDF.stringWidth(text, font_name, font_size)
			x = self.get_x(centered=centered) - (text_width / 2)
		
		new_x, new_y = self.write(x, y, text, font_name, font_size)

		return new_x, new_y

	# def WR_LINE(self, x=int, y=int, TXT=str):
	# 	'''
	# 	Writte a line text with the default font config
	# 	'''
	# 	xpos = x
	# 	ypos = y
	# 	words = TXT.split(chr(32))
	# 	for word in words:
	# 		wordWidth = pdfmetrics.stringWidth(word + " ", self.PDF._fontname, self.PDF._fontsize)
	# 		if xpos + wordWidth > self.marginRight:
	# 			xpos = self.marginLeft
	# 			ypos -= (self.defaultSize + self.spacing)
	# 		self.PDF.drawString(xpos,ypos,word)
	# 		xpos += wordWidth + 1
	# 	self.row = ypos - (self.defaultSize + self.spacing)
	
	# def WR_LINE_CENTERED(self, x=int, y=int, TXT=str):
	# 	self.PDF.drawCentredString(x,y,TXT)
	# 	self.row -= (self.PDF._fontsize + self.spacing)
	
	# def WR_MULTILINE(self):
	# 	'''
	# 	INCOMPLETE
	# 	'''
	# 	# text = self.PDF.beginText(40, 680)
	# 	# text.setFont("Courier", 18)
	# 	# text.setFillColor(colors.red)
	# 	# for line in textLines:
	# 	# 	text.textLine(line)
	# 	# self.PDF.drawText(text)
	# 	pass

	# def WR_HEADER(self, x=int, y=int, TXT=str, filling=None, fontType=fontTypes.bold, size=15):
	# 	'''
	# 	hay que controlar el ancho del HEADER
	# 	'''
	# 	ypos = y - size
	# 	## FILLING
	# 	self.PDF.setFillColorRGB(100, 100, 100)
	# 	# textWidth = pdfmetrics.stringWidth(TXT + "  ", fontType, size)
	# 	self.PDF.setLineWidth(0)
	# 	self.PDF.setLineCap(0)
	# 	# self.PDF.rect(report.marginLeft,y,textWidth,size, fill=1)
	# 	# self.PDF.rect(self.marginLeft,ypos,self.marginRight-30,size, fill=1)
	# 	## TEXT
	# 	self.PDF.setFillColor(colors.black)
	# 	self.PDF.setFont(fontType, size)
	# 	self.PDF.drawString(x,ypos,TXT)
	# 	self.row = ypos
	# 	self.WR_SPACING(2)
	# 	## SET DEFAULT
	# 	self.SET_DEFAULT()

	# def WR_RICHTEXT(self, x=int, y=int, TXT_LIST=list):
	# 	'''
	# 	Escribe una linea tanto en formato str como con richText respetando el ancho de la página
	# 	'''
	# 	xpos = x
	# 	ypos = y
	# 	for item in TXT_LIST:
	# 		# Set Text
	# 		if type(item) == str:
	# 			txt = item
	# 		if type(item) == int or type(item) == float:
	# 			txt = str(item)
	# 		if type(item) == richText:
	# 			self.SET_FONT(item.font, item.size)
	# 			self.SET_COLOR(item.color)
	# 			txt = str(item.value)
	# 		# 
	# 		words = txt.split(chr(32))
	# 		for word in words:
	# 			wordWidth = pdfmetrics.stringWidth(word + " ", self.PDF._fontname, self.PDF._fontsize)
	# 			if xpos + wordWidth > self.marginRight:
	# 				xpos = self.marginLeft
	# 				ypos -= (self.defaultSize + self.spacing)
	# 			self.PDF.drawString(xpos,ypos,word)
	# 			xpos += wordWidth + 1
	# 		# Return to default font config
	# 		self.SET_DEFAULT()
	# 	# 
	# 	self.row = ypos - (self.defaultSize + self.spacing)

	# def WR_HLINE(self, y=int, lineWidth: int=1.5):
	# 	'''
	# 	Draw a horizontal line
	# 	'''
	# 	self.PDF.setLineWidth(lineWidth) # Line Width
	# 	self.PDF.line(self.marginLeft, y, self.marginRight, y)
	# 	self.WR_SPACING(2)

	# def WR_SPACING(self, lines=1):
	# 	self.row -= (self.spacing * 2 * lines)
	
	# def SET_DEFAULT(self):
	# 	'''
	# 	Return to default font config
	# 	'''
	# 	self.SET_FONT(self.defaultFont, self.defaultSize)
	# 	self.PDF.setFillColor(self.defaulColor)

def from_markdown(md_path: str, pdf_path: str):
	''' ⚠️INCOMPLETE
	Create an .pdf document from MarkDown File
	'''
	pass