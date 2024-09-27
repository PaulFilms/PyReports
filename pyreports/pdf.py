'''
Toolkit with simplified functions and methods for create .pdf Reports

Comming Soon
'''
__update__ = '2024.09.27'

from dataclasses import dataclass

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import pagesizes
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


## TOOLS
## _________________________________________________________________________________________________________________

@dataclass
class fontTypes(str):
	'''
	DataClass to define Font Types in text format
	'''
	normal: str = "Normal"
	bold: str = "Bold"
	italic: str = "Italic"
	bold_italic: str = "Bold_Italic"

@dataclass
class richText():
	'''
	DataClass for defining the content and formatting of a text string
	'''
	value: str = ""
	font: fontTypes = fontTypes.normal
	size: float = 8
	color: colors = colors.black
		
class PDFREPORT:
	'''
	Un A-4 a 72 ppp    595 x 842
	Default Font: Arial
	'''
	def __init__(self, filePath, docTitle: str, defaultFont=fontTypes.normal, defaultSize=8, defaulColor=colors.black):
		self.filePath = filePath
		self.PDF = canvas.Canvas(self.filePath + ".pdf")

		## DOCUMENT NAME
		if docTitle:
			self.PDF.setTitle(docTitle)
		else:
			self.PDF.setTitle("REPORT")
		
		## FONTS
		# pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
		# pdfmetrics.registerFont(TTFont('Times_new-BoldItalic', 'timesbi.ttf', subfontIndex=3))
		pdfmetrics.registerFont(TTFont('Normal', 'arial.ttf'))
		pdfmetrics.registerFont(TTFont('Bold', 'arialbd.ttf'))
		pdfmetrics.registerFont(TTFont('Italic', 'ariali.ttf'))
		pdfmetrics.registerFont(TTFont('Bold_Italic', 'arialbi.ttf'))
		self.defaultFont = defaultFont
		self.defaultSize = defaultSize
		self.defaulColor = defaulColor
		# self.SET_FONT(fontTypes.normal, 8)
		self.SET_DEFAULT()
		
		## PAGE SIZE / MARGINS
		pageSize = pagesizes.landscape(pagesizes.A4)
		self.pageHeight = pageSize[0] # 841.88
		self.pageWidth = pageSize[1] # 595.27
		self.marginLeft = 45
		self.marginRight = self.pageWidth - self.marginLeft
		self.marginTop = 10
		self.marginBottom = self.pageHeight - 10
		self.row = 820 - self.marginTop
		self.spacing = 5

		## Get objects
		# lineWidth = self.PDF._lineWidth
		# print(lineWidth)
		# fillColor = self.PDF._fillColorObj
		# print(fillColor)

		## SAVING THE .PDF FILE
		# self.PDF.save()
		pass

	def WR_LINE(self, x=int, y=int, TXT=str):
		'''
		Writte a line text with the default font config
		'''
		xpos = x
		ypos = y
		words = TXT.split(chr(32))
		for word in words:
			wordWidth = pdfmetrics.stringWidth(word + " ", self.PDF._fontname, self.PDF._fontsize)
			if xpos + wordWidth > self.marginRight:
				xpos = self.marginLeft
				ypos -= (self.defaultSize + self.spacing)
			self.PDF.drawString(xpos,ypos,word)
			xpos += wordWidth + 1
		self.row = ypos - (self.defaultSize + self.spacing)
	
	def WR_LINE_CENTERED(self, x=int, y=int, TXT=str):
		self.PDF.drawCentredString(x,y,TXT)
		self.row -= (self.PDF._fontsize + self.spacing)
	
	def WR_MULTILINE(self):
		'''
		INCOMPLETE
		'''
		# text = self.PDF.beginText(40, 680)
		# text.setFont("Courier", 18)
		# text.setFillColor(colors.red)
		# for line in textLines:
		# 	text.textLine(line)
		# self.PDF.drawText(text)
		pass

	def WR_HEADER(self, x=int, y=int, TXT=str, filling=None, fontType=fontTypes.bold, size=15):
		'''
		hay que controlar el ancho del HEADER
		'''
		ypos = y - size
		## FILLING
		self.PDF.setFillColorRGB(100, 100, 100)
		# textWidth = pdfmetrics.stringWidth(TXT + "  ", fontType, size)
		self.PDF.setLineWidth(0)
		self.PDF.setLineCap(0)
		# self.PDF.rect(report.marginLeft,y,textWidth,size, fill=1)
		# self.PDF.rect(self.marginLeft,ypos,self.marginRight-30,size, fill=1)
		## TEXT
		self.PDF.setFillColor(colors.black)
		self.PDF.setFont(fontType, size)
		self.PDF.drawString(x,ypos,TXT)
		self.row = ypos
		self.WR_SPACING(2)
		## SET DEFAULT
		self.SET_DEFAULT()

	def WR_RICHTEXT(self, x=int, y=int, TXT_LIST=list):
		'''
		Escribe una linea tanto en formato str como con richText respetando el ancho de la página
		'''
		xpos = x
		ypos = y
		for item in TXT_LIST:
			# Set Text
			if type(item) == str:
				txt = item
			if type(item) == int or type(item) == float:
				txt = str(item)
			if type(item) == richText:
				self.SET_FONT(item.font, item.size)
				self.SET_COLOR(item.color)
				txt = str(item.value)
			# 
			words = txt.split(chr(32))
			for word in words:
				wordWidth = pdfmetrics.stringWidth(word + " ", self.PDF._fontname, self.PDF._fontsize)
				if xpos + wordWidth > self.marginRight:
					xpos = self.marginLeft
					ypos -= (self.defaultSize + self.spacing)
				self.PDF.drawString(xpos,ypos,word)
				xpos += wordWidth + 1
			# Return to default font config
			self.SET_DEFAULT()
		# 
		self.row = ypos - (self.defaultSize + self.spacing)

	def WR_HLINE(self, y=int, lineWidth: int=1.5):
		'''
		Draw a horizontal line
		'''
		self.PDF.setLineWidth(lineWidth) # Line Width
		self.PDF.line(self.marginLeft, y, self.marginRight, y)
		self.WR_SPACING(2)

	def WR_SPACING(self, lines=1):
		self.row -= (self.spacing * 2 * lines)

	def IMAGE_INSERT(self, imageFile, x=int, y=int, ):
		'''
		INCOMPLETE
		Hay que añadir la relacion de aspecto
		'''
		## drawing a image at the specified (x.y) position
		image = ImageReader(imageFile)
		image = imageFile
		self.PDF.drawInlineImage(image, x, y)
		pass

	def FONT_REGISTRER(self, fontName=str, fontTTF="Arial.ttf"):
		pdfmetrics.registerFont(TTFont(fontName, fontTTF))
	
	def SET_DEFAULT(self):
		'''
		Return to default font config
		'''
		self.SET_FONT(self.defaultFont, self.defaultSize)
		self.PDF.setFillColor(self.defaulColor)

	def SET_FONT(self, fontType: fontTypes, fontSize: int):
		'''
		Set the font Type and font Size
		'''
		self.PDF.setFont(fontType, fontSize)

	def SET_COLOR(self, color=colors, rgb=tuple):
		'''
		INCOMPLETE:
			- Hay que crear un dataclass con el color
		'''
		# if color == "black": self.PDF.setFillColorRGB(0, 0, 0)
		# if color == "blue": self.PDF.setFillColorRGB(0, 0, 255)
		# if color == "red": self.PDF.setFillColorRGB(255, 0, 0)
		# if color == "green": self.PDF.setFillColorRGB(0, 255, 0)
		# if color == "grey": self.PDF.setFillColorRGB(160, 160, 160)
		self.PDF.setFillColor(color)
		color_rgb = self.PDF._fillColorObj
		# print("SET_COLOR:", color_rgb)
		pass