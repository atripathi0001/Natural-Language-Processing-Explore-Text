import wx
import nltk 
from nltk import FreqDist
from nltk.collocations import	*
import ner 
import re
from re import finditer
from itertools import tee, islice, izip, chain, repeat
import nltk.corpus  
 
val = 0
filePath = ""
'''
def kwic(text, tgtword, width=5):
    'Find all occurrences of tgtword and show the surrounding context'
    matches = (mo.span() for mo in finditer(r"[A-Za-z\'\-]+", text))
    padded = chain(repeat((0,0), width), matches, repeat((-1,-1), width))
    t1, t2, t3 = tee((padded), 3)
    t2 = islice(t2, width, None)
    t3 = islice(t3, 2*width, None)
    for (start, _), (i, j), (_, stop) in izip(t1, t2, t3):
        if text[i: j] == tgtword:
            context = text[start: stop]
            yield context
'''
def kwic(target_word, pessage, left_margin = 5, right_margin = 5):
    tokens = nltk.word_tokenize(pessage)
    text = nltk.Text(tokens)
    c = nltk.ConcordanceIndex(text.tokens, key = lambda s: s.lower())
    concordance_txt = ([text.tokens[map(lambda x: x-5 if (x-left_margin)>0 else 0,[offset])[0]:offset+right_margin]
                        for offset in c.offsets(target_word)])
    return [''.join([x+' ' for x in con_sub]) for con_sub in concordance_txt]

def alpha_filter(w):
  	# pattern to match word of non-alphabetical characters
  	pattern = re.compile('^[^a-z]+$')
  	if (pattern.match(w)):
    		return True
  	else:
    		return False

class ExampleFrame(wx.Frame):
    def __init__(self, parent):
	wx.Frame.__init__(self, None,  pos=(0,0), size=(260,180))
	
	self.Maximize(True)
		
        self.panel = wx.Panel(self)     
        self.quote = wx.StaticText(self.panel, -1,label="Explore Text with Corpus Statistics",style=wx.ALIGN_CENTRE)
	self.quote.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.quote.SetSize(self.quote.GetBestSize())

        self.result = wx.StaticText(self.panel, label="")
        self.result.SetForegroundColour(wx.RED)
	self.browseButton = wx.Button(self.panel, label="Select File to Process")

        self.button = wx.Button(self.panel, label="KWIC (use lowercase)")
	self.search = wx.TextCtrl(self.panel, size=(240, -1))
        self.lblname = wx.StaticText(self.panel, label="Select the number of items to view :\nItems are in order by highest frequency\nor leave blank to view all.")
        self.editname = wx.TextCtrl(self.panel, size=(140, -1))
	self.viewWords = wx.Button(self.panel, wx.ID_CLOSE, "View Words")
	self.viewBigrams = wx.Button(self.panel, wx.ID_CLOSE, "View Bigrams")
	self.viewPersons = wx.Button(self.panel, wx.ID_CLOSE, "View Persons")
	self.OutLabel = wx.StaticText(self.panel, -1, "Output")
	self.OutLabel.SetForegroundColour((255,0,0))  
	self.OutLabel.SetBackgroundColour((255,255,255))
	self.processing = wx.StaticText(self.panel, label="")
	self.processing.SetForegroundColour((0,255,0))  
	self.processing.SetBackgroundColour((255,255,255))

	self.cb1 = wx.CheckBox(self.panel, -1, 'Person', (10, 10))
        self.cb1.SetValue(False)
	self.cb2 = wx.CheckBox(self.panel, -1, 'Organization', (10, 10))
        self.cb2.SetValue(False)
	self.cb3 = wx.CheckBox(self.panel, -1, 'Location', (10, 10))
        self.cb3.SetValue(False)

       

        # Set sizer for the frame, so we can change frame size to match widgets
        self.windowSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)    
	self.windowSizer.Add(self.panel, 1, wx.ALL)            

        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(25, 25)
        self.sizer.Add(self.quote, (0, 4))
	self.sizer.Add(self.browseButton, (1, 0), (1, 2), flag=wx.EXPAND)
	self.sizer.Add(self.result, (0, 1))
        self.sizer.Add(self.lblname, (2, 0))
        self.sizer.Add(self.editname, (2, 1))
        self.sizer.Add(self.viewWords, (3, 0), (1, 2), flag=wx.EXPAND)
	self.sizer.Add(self.viewBigrams, (4, 0), (1, 2), flag=wx.EXPAND)
	self.sizer.Add(self.viewPersons, (5, 0), (1, 2), flag=wx.EXPAND)
	self.sizer.Add(self.cb1, (6, 1))
	self.sizer.Add(self.cb2, (7, 1))
	self.sizer.Add(self.cb3, (8, 1))
        self.sizer.Add(self.button, (9, 0), (1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.search, (10, 0), (1, 2), flag=wx.EXPAND)
	self.sizer.Add(self.OutLabel, (2, 2),(10,3))
	self.sizer.Add(self.processing, (1,2))



        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        # Use the sizers
        self.panel.SetSizerAndFit(self.border)  
        self.SetSizerAndFit(self.windowSizer)  

        # Set event handlers
        self.button.Bind(wx.EVT_BUTTON, self.Search)
	self.browseButton.Bind(wx.EVT_BUTTON, self.Browse)
	self.viewWords.Bind(wx.EVT_BUTTON, self.ViewWords)
	self.viewBigrams.Bind(wx.EVT_BUTTON, self.ViewBigrams)
	self.viewPersons.Bind(wx.EVT_BUTTON, self.ViewPersons)
 	wx.EVT_CHECKBOX(self, self.cb1.GetId(), self.SetCB1)
	wx.EVT_CHECKBOX(self, self.cb2.GetId(), self.SetCB2)
	wx.EVT_CHECKBOX(self, self.cb3.GetId(), self.SetCB3)

    def Browse(self, event):
        openFileDialog = wx.FileDialog(self, "Open file", "", "","", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	openFileDialog.ShowModal()
	global filePath 
        filePath = openFileDialog.GetPath()
	print "File selected : ",filePath
	return filePath
        openFileDialog.Destroy()

    def SetCB1(self, event):
	print "Check box 1 value chnaged to ",
	val = self.cb1.GetValue()	
	print val

    def SetCB2(self, event):
	print "Check box 2 value chnaged to ",
	val = self.cb2.GetValue()	
	print val

    def SetCB3(self, event):
	print "Check box 3 value chnaged to ",
	val = self.cb3.GetValue()	
	print val

    def ViewWords(self, event):
	self.processing.SetLabel('Procrssing....')
	global filePath 
	if filePath == "":
		self.OutLabel.SetLabel("Output\n\nPlease select file.") 
		return
	stopwords = nltk.corpus.stopwords.words('english')
	f = open(filePath, 'r').read()
	tokens	= nltk.word_tokenize(f)
	words	= [w.lower() for w in tokens]
	alphawords = [w for w in words if not alpha_filter(w)]
	stoppedwords = [w for w in alphawords if not w in stopwords]
	fdist	= FreqDist(stoppedwords)
	inp = self.editname.GetValue()
	if inp == '' or inp == 0 or inp == None:
		inp =10000 
	val = int(inp)
	outstr = "Output : \nWord\t\t --> \t Frequency\n"
	self.OutLabel.SetLabel(str(fdist.most_common(val)))
	for word in fdist.most_common(val):
		print	word 
		outstr = outstr +str(word[0]).ljust(40)+ str(word[1])+"\n"
	self.OutLabel.SetLabel(str(outstr))
	self.processing.SetLabel('Done.')

    def ViewBigrams(self, event):
	self.processing.SetLabel('Processing....')
	global filePath 
	if filePath == "":
		self.OutLabel.SetLabel("Output\n\nPlease select file.") 
		return
	stopwords = nltk.corpus.stopwords.words('english')
	f = open(filePath, 'r').read()
	tokens	= nltk.word_tokenize(f)
	words	= [w.lower() for w in tokens]
	alphawords = [w for w in words if not alpha_filter(w)]
	stoppedwords = [w for w in alphawords if not w in stopwords]
	bigram_measures	= nltk.collocations.BigramAssocMeasures()
	finder	= BigramCollocationFinder.from_words(stoppedwords)
	scored	= finder.score_ngrams(bigram_measures.raw_freq)
	outstr = "Output : \nBigram \t\t-->\t\t\t\t\tFrequency\n"
	inp = self.editname.GetValue()
	if inp == '' or inp == 0 or inp == None:
		inp =10000 
	val = int(inp)
	for word in scored[:val]:
		print word
		outstr = outstr + str(word[0])+"\t --> \t\t\t"+ str(word[1])+"\n"
	self.OutLabel.SetLabel(str(outstr)) 
	self.processing.SetLabel('Done.')

    def ViewPersons(self, event):
	self.processing.SetLabel('Processing....')
	global filePath 
	if filePath == "":
		self.OutLabel.SetLabel("Output\n\nPlease select file.") 
		return
	f = open(filePath, 'r').read()
	# Port Number can be updated according to the value initilized while running the server 
	tagger = ner.SocketNER(host='localhost', port=8080)
	output = tagger.get_entities(str(f))
	outstr = "Result\n"
	inp = self.editname.GetValue()
	if inp == '' or inp == 0 or inp == None:
		inp =10000 
	val = int(inp)
	print output
	val1 = self.cb1.GetValue()
	val2 = self.cb2.GetValue()
	val3 = self.cb3.GetValue()	
	if not val1 and not val2 and not val3:
		for key, value in output.items():
			#print word
			subStr =''
			c = 0
			for v in value:
				if v not in subStr:
					c = c+1
					subStr = subStr  + v+", "
					if c == 7:
						c =0
						subStr = subStr  + "\n"
			outstr = outstr + str(key)+":\n"+str(subStr[:-2])+"\n\n"
	else:
		for key, value in output.items():
			if val1 and key == "PERSON":
			#print word
				subStr =''
				c = 0
				for v in value:
					if v not in subStr:
						c = c+1
						subStr = subStr  + v+", "
						if c == 7:
							c =0
							subStr = subStr  + "\n"
		 		outstr = outstr + str(key)+":\n"+str(subStr[:-2])+"\n\n"
				
			if val2 and key == "ORGANIZATION":
					#print word
					subStr =''
					c = 0
					for v in value:
						if v not in subStr:
							c = c+1
							subStr = subStr  + v+", "
							if c == 7:
								c =0
								subStr = subStr  + "\n"
					outstr = outstr + str(key)+":\n"+str(subStr[:-2])+"\n\n"
		
			if val3 and key == "LOCATION":
				#print word
				subStr =''
				c = 0
				for v in value:
					if v not in subStr:
						c = c+1
						subStr = subStr  + v+", "
						if c == 7:
							c =0
							subStr = subStr  + "\n"
				outstr = outstr + str(key)+":\n"+str(subStr[:-2])+"\n\n"
		
	if outstr =="" or outstr == None or outstr =="Result\n":
		outstr = "Nothing found."	
	print outstr	
	self.OutLabel.SetLabel(str(outstr))
	self.processing.SetLabel('Done.')
	

    def Search(self, e):
	self.processing.SetLabel('Processing....')
	result = 'Matched lines are : \n\n'
	searchTerm = str(self.search.GetValue())
	print "Search term : ",searchTerm

	if searchTerm == '' or searchTerm == None:
		result = "Output\nPlease enter search string."
		self.OutLabel.SetLabel(result)
		return
	global filePath 
	if filePath == "":
		self.OutLabel.SetLabel("Output\n\nPlease select file.") 
		return
	f = open(filePath, 'r').read()
	#result =  list(kwic(f, searchTerm))
	#output = ''
	#for line in result:
		#output = output + line + "\n"
 	results = kwic(searchTerm, f)
	for r in results:
   		  result = result + "....."+r+"....." +"\n\n"
		  print result
	if "..." not in result:
		result = "No match found."
	self.OutLabel.SetLabel(str(result))
	print "Result : \n",result
	self.processing.SetLabel('Done.')

	

app = wx.App(False)
frame = ExampleFrame(None)
frame.Show()
frame.SetTitle('Explore Text')
app.MainLoop()
