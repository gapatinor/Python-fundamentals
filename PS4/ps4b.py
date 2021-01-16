import string

#-------------Helper functions----------------------------

def load_words(file_name):
  #print("Loading word list from file...")
  # inFile: file
  inFile = open(file_name, 'r')
  # wordlist: list of strings
  wordlist = []
  for line in inFile:
    wordlist.extend([word.lower() for word in line.split(' ')])
  #print len(wordlist), "words loaded."
  return wordlist

def is_word(word_list, word):
  '''Determines if word is a valid word, ignoring
    capitalization and punctuation'''
  word = word.lower()
  word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
  return word in word_list

def get_story_string():
  """Returns: a story in encrypted text. """
  f = open("story.txt", "r")
  story = str(f.read())
  f.close()
  return story

WORDLIST_FILENAME = 'words.txt'

#--------------------------------------------------------------------------

class Message(object):
  def __init__(self, text):
   '''Initializes a Message object text (string): the message's text'''
   self.message_text=text
   self.valid_words=load_words(WORDLIST_FILENAME)

  def get_message_text(self):
    '''Used to safely access self.message_text outside of the class'''
    return self.message_text
       
  def get_valid_words(self):
   '''Used to safely access a copy of self.valid_words outside of the class.'''
   return self.valid_words
    
  def build_shift_dict(self, shift):
   '''Creates a dictionary that can be used to apply a cipher to a letter.
       The dictionary maps every uppercase and lowercase letter to a
       character shifted down the alphabet by the input shift.'''

   alpha="abcdefghijklmnopqrstuvwxyz"
   ALPHA="ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
   maps1,maps2,maps={},{},{}
  
   for ch in alpha:
    nold=alpha.find(ch)
    nnew=nold+shift
    if(nnew>25): nnew=nnew-26
    ch_new=alpha[nnew]
    maps1[ch]=ch_new
 
   for ch in ALPHA:
    nold=ALPHA.find(ch)
    nnew=nold+shift
    if(nnew>25): nnew=nnew-26
    ch_new=ALPHA[nnew]
    maps2[ch]=ch_new

   maps=maps1.copy()
   maps.update(maps2) #merge dictionaries
   return maps

  def apply_shift(self, shift):
    ''' Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift'''
    maps=self.build_shift_dict(shift)
    st=""
    for e in self.get_message_text(): 
      if(e.isalpha()):
        st+=str(maps[e])
      else: st+=str(e) 
    return st
    
    
class PlaintextMessage(Message):
  def __init__(self, text, shift):
   '''Initializes a PlaintextMessage object text (string): the message's text
     shift (integer): the shift associated with this message'''
   
   Message.__init__(self,text) #initially we must build an object to apply the methods apply_shift...
   self.text=text
   self.encryption_dict=self.build_shift_dict(shift)
   self.message_text_encrypted=self.apply_shift(shift)
   Message.__init__(self,self.message_text_encrypted) #we must call again the constructor to create obj
   
  def get_shift(self):
    '''Used to safely access self.shift outside of the class'''
    return self.shift

  def get_encryption_dict(self):
    '''Used to safely access a copy self.encryption_dict outside of the class'''
    return self.encryption_dict 

  def get_message_text_encrypted(self):
    '''Used to safely access self.message_text_encrypted outside of the class'''
    return  self.message_text_encrypted

  def change_shift(self, shift):
    ''' Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.'''
    text=self.text
    PlaintextMessage.__init__(self,text,shift)

class CiphertextMessage(Message):
 def decrypt_message(self):
  '''
     Decrypt self.message_text by trying every possible shift value
     and find the "best" one. We will define "best" as the shift that
     creates the maximum number of real words when we use apply_shift(shift)
     on the message text. If s is the original shift value used to encrypt
     the message, then we would expect 26 - s to be the best shift value 
     for decrypting it.'''

  def build_list(words):
    word_objects=[]
    for word in words:
     word_objects.append(Message(word))
    return word_objects  

  text=self.get_message_text()
  word_text=text.split()
  word_objects=build_list(word_text)

  matchesBest=0
  for s in range(26):
   matches=0
   for elem in word_objects:
    word=elem.apply_shift(s)
    if(is_word(wordlist,word)): 
     matches+=1
   if(matches>matchesBest): 
    matchesBest=matches
    shift=s
 
  best_guess=""
  for elem in word_objects:
   word=elem.apply_shift(shift)
   best_guess+=word+" "
  shift=26-shift
  return best_guess,shift 
  

 
wordlist=load_words('words.txt')

message="We try to learn to code. Using,  platforms?"
plain=PlaintextMessage(message,3)
cipher_str=plain.get_message_text_encrypted()

cipher=CiphertextMessage(cipher_str)
print cipher.get_message_text()
solution=cipher.decrypt_message()
print solution[0],"shift",solution[1],"\n"

story_text=get_story_string()
cipher=CiphertextMessage(story_text)
solution=cipher.decrypt_message()
print solution[0],"shift",solution[1],"\n"






  
