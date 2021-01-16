import string
from ps4a import get_permutations

#--------- Helper functions ---------------------------
def load_words(file_name):
  '''file_name (string): the name of the file containing 
    the list of words to load'''
    
  # inFile: file
  inFile = open(file_name, 'r')
  # wordlist: list of strings
  wordlist = []
  for line in inFile:
    wordlist.extend([word.lower() for word in line.split(' ')])
   
  return wordlist

def is_word(word_list, word):
  '''Determines if word is a valid word, ignoring
    capitalization and punctuation'''
  word = word.lower()
  word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
  return word in word_list

#------ end helper functions -------------------------------

WORDLIST_FILENAME = 'words.txt'

VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
  def __init__(self, text):
    '''Initializes a SubMessage object'''
    self.message_text=text
    self.valid_words=load_words("words.txt")    

  def get_message_text(self):
    '''Used to safely access self.message_text outside of the class'''
    return self.message_text  

  def get_valid_words(self):
    '''Used to safely access a copy of self.valid_words outside of the class.'''
    return self.valid_words

  def build_transpose_dict(self, vowels_permutation):
    maps,mapsv,MAPSV={},{},{}
    for i in range(len(VOWELS_LOWER)):
     mapsv[VOWELS_LOWER[i]]=(vowels_permutation[i]).lower()
     MAPSV[VOWELS_UPPER[i]]=(vowels_permutation[i]).upper()
    maps=mapsv.copy()
    maps.update(MAPSV) #merge dictionaries
    return maps

  def apply_transpose(self, transpose_dict):
    '''transpose_dict (dict): a transpose dictionary 
        Returns: an encrypted version of the message text, based 
        on the dictionary'''
    
    text=self.get_message_text()
    message=""
    for ch in text:
     if(ch in VOWELS_LOWER):
      message+=transpose_dict[ch]
     elif(ch in VOWELS_UPPER):
      message+=transpose_dict[ch]
     else: message+=ch
    return message

class EncryptedSubMessage(SubMessage):
  def decrypt_message(self):
    '''Attempt to decrypt the encrypted message'''
    
    permutations=get_permutations("aeiou")
    text=self.get_message_text()
    words_text=text.split()
    bestMatche=0
    for permut in permutations:
     dic=self.build_transpose_dict(permut)
     dec_message=self.apply_transpose(dic)
     matches=0
     for internal_word in dec_message.split():
       if(is_word(word_list, internal_word)): 
        matches+=1
     if(matches>bestMatche):
       bestMatche=matches
       bestPerm=permut
       bestDecripted=dec_message 
    return bestDecripted
    
 
word_list=load_words("words.txt")
mes=SubMessage("Hello, WOrld! we out of it")
print "original message: ",mes.get_message_text()

dic=mes.build_transpose_dict("eaiuo")
mess=mes.apply_transpose(dic)
print "cypher message: ", mess

encripted=EncryptedSubMessage(mess)
print encripted.decrypt_message()








