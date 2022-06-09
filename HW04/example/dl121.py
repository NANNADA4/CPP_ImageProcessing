# -*- coding: cp949 -*-
# filename : paint.pyw
# 간단한 이미지 프로세싱 프로그램

from Tkinter import *
import tkFileDialog, tkMessageBox
import Image, ImageTk
import math
import numpy.fft

def FCT(array):
	add=array[1:-1]
	add.reverse()
	res=numpy.fft.rfft(array+add)
	return [ num.real/(len(array)-1) for num in res ]

def IFCT(array):
	res=numpy.fft.irfft(array)[0:len(array)]
	return [ num.real*(len(array)-1) for num in res ]

class App:
	def __init__(self):
		self.root=Tk()
		self.menu=Menu(self.root)
		self.root.config(menu=self.menu);
		self.label=Label(self.root, text="", width=50, height=20)
		self.label.pack()

		self.filemenu=Menu(self.menu)
		self.menu.add_cascade(label=u"파일", menu=self.filemenu)
		self.filemenu.add_command(label=u"열기", command=self.OpenFile, accelerator="Ctrl+O")
		self.filemenu.add_separator()
		self.filemenu.add_command(label=u"종료", command=self.Quit, accelerator="Ctrl+Q")

		self.editmenu=Menu(self.menu)
		self.menu.add_cascade(label=u"편집", menu=self.editmenu)
		self.editmenu.add_command(label=u"DCT", command=self.DCT, accelerator="Ctrl+T")
		self.editmenu.add_command(label=u"IDCT", command=self.IDCT, accelerator="Ctrl+I")

		self.root.bind("<Control-o>",self.OpenFile)
		self.root.bind("<Control-q>",self.Quit)
		self.root.bind("<Control-t>",self.DCT)
		self.root.bind("<Escape>",self.Quit)
		self.root.mainloop()
		self.Result=None

	def OpenFile(self,event=None):
		self.filename=tkFileDialog.askopenfilename()
		if(self.filename==""):
			return
		try:
			self.image=Image.open(self.filename)
		except:
			tkMessageBox.showerror(u"오류 !","파일 열기에 실패했습니다")
		else:
			self.pixel=self.image.load()
			self.label.image=ImageTk.PhotoImage(self.image)
			Label.__init__(self.label,self.root,image=self.label.image,bd=0)
			self.label.pack()

	def Quit(self,event=None):
		self.root.destroy()

	def DCT(self,event=None):
		image=self.image.convert("L")	# 흑백 이미지로 만들어버린다
		image2=Image.new("L",image.size)	# 새 이미지를 만든다. (결과)

		pix=image.load()	# 원본 이미지의 PixelAccess 객체
		pix2=image2.load()	# 결과 이미지의 PixelAccess 객체

		N=image.size[0]	# 가로 길이
		M=image.size[1]	# 세로 길이
		mid=[FCT([pix[n,m] for n in range(N)]) for m in range(M)]
		res=[FCT([mid[m][n] for m in range(M)]) for n in range(N)]
	
		# result에 있는 숫자들의 평균 * 0.1 - 화면에 그림으로 보여주기 위한 적절한 숫자
		Scale=sum([sum([abs(x) for x in list])/len(list) for list in res])/len(res)*0.1	
		# 결과를 픽셀값 0~255에 맞게 재배치함
		for i in range(N):
			for j in range(M):	
				pix2[i,j]=res[i][j]/Scale+128	# 회색(128)을 0으로 해서 음수는 어둡게, 양수는 밝게 이미지를 표시함
		print res[0][0]
		self.Result=res		# DCT결과를 저장함.

		self.image=image2;
		self.label.image=ImageTk.PhotoImage(self.image)
		Label.__init__(self.label,self.root,image=self.label.image,bd=0)
		self.label.pack()


	def IDCT(self,event=None):
		image=self.image.convert("L")	# 흑백 이미지로 만들어버린다
		image2=Image.new("L",image.size)	# 새 이미지를 만든다. (결과)

		pix=image.load()	# 원본 이미지의 PixelAccess 객체
		pix2=image2.load()	# 결과 이미지의 PixelAccess 객체

		N=image.size[0]	# 가로 길이
		M=image.size[1]	# 세로 길이

		mid=[IFCT([self.Result[n][m] for n in range(N)]) for m in range(M)]	# 중간과정
		res=[IFCT([mid[m][n] for m in range(M)]) for n in range(N)]		# 최종결과

		for n in range(N):
			for m in range(M):
				pix2[n,m]=res[n][m]		# 결과를 PixelAccess객체에 저장

		self.image=image2;
		self.label.image=ImageTk.PhotoImage(self.image)
		Label.__init__(self.label,self.root,image=self.label.image,bd=0)
		self.label.pack()


App()
