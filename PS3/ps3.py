import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def load_words():
 '''Returns a list of valid words. Words are strings of lowercase letters.'''
 print "Loading word list from file..."
 # inFile: file
 inFile = open(WORDLIST_FILENAME, 'r')
 # wordlist: list of strings
 wordlist = []
 for line in inFile:
   wordlist.append(line.strip().lower())
 print len(wordlist), "words loaded."
 return wordlist

def get_frequency_dict(sequence):
  '''
  Returns a dictionary where the keys are elements of the sequence
  and the values are integer counts, for the number of times that
  an element is repeated in the sequence. sequence: string or list
  return: dictionary'''
    
  freq = {}
  for x in sequence:
    freq[x] = freq.get(x,0) + 1
  return freq


def get_word_score(word, n):
  '''Returns the score for a word. Assumes the word is a valid word.'''
  s1=0
  for e in word:
    if(e!="*"): s1+=SCRABBLE_LETTER_VALUES[e]
  s2=abs(HAND_SIZE*len(word)-3*(n-len(word)))
  return s1*s2    


def deal_hand(n,wildcard=False):
  '''Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.'''
    
  hand={}
  num_vowels = int(math.ceil(n / 3))

  for i in range(num_vowels):
    x = random.choice(VOWELS)
    hand[x] = hand.get(x, 0) + 1
    
  for i in range(num_vowels, n):    
    x = random.choice(CONSONANTS)
    hand[x] = hand.get(x, 0) + 1
    
  if(wildcard):
   for x in hand.keys():
    if(x in VOWELS and hand[x]==1):
     hand["*"]=hand[x]
     hand.pop(x)
     break 
  return hand

def display_hand(hand):
  '''Displays the letters currently in the hand.'''
  s=""   
  for letter in hand.keys():
   for j in range(hand[letter]):
     s+= str(letter)
  return s                      

def update_hand(hand, word):
 hand=hand.copy()
 for k in word:
  if(k in hand.keys()):
   hand[k]=hand[k]-1 
   if(hand[k]==0): hand.pop(k,None)
 return hand

def is_valid_word(word, hand, word_list):
 '''Returns True if word is in the word_list and is entirely
     composed of letters in the hand. Otherwise, returns False.
     Does not mutate hand or word_list.'''
 
 for c in word:
  if(c not in hand): return False

 for c in word:
  if(c=="*"):
   for v in VOWELS:
    w=word.replace(str(c),str(v))
    if(w in word_list): return True
 if(word in word_list): return True
 else: return False   


def play_hand(hand, word_list):
 totalScore=0
 while(True):
  if(len(display_hand(hand))==0):
   print "Ran out of letters. Total score in this hand:",totalScore,"points","\n","-------"
   break
  print "current hand:", display_hand(hand)
  
  word=raw_input("Enter word, or !! to indicate that you are finished: ")
  if(word=="!!"):
   print "Total Score in this hand:",totalScore, "points","\n","-------"
   break
  
  if(is_valid_word(word,hand,word_list)):
   n=len(display_hand(hand))
   totalScore+=get_word_score(word, n)
   print word, "earned", get_word_score(word, n), "points.Total:",totalScore,"points","\n"
  else: print word, "is not a valid word. Please choose another word."
  hand=update_hand(hand, word)
 return totalScore

def substitute_hand(hand, letter):
 hand=hand.copy()
 alpha="abcdefghijklmnopqrstuvwxyz"
 if(letter in hand):
   alpha=alpha.replace(letter,"")
   for e in hand.keys():
    alpha=alpha.replace(e,"")
   x=random.choice(alpha)
   hand[x]=hand[letter]
   hand.pop(letter,None)
 return hand

def play_game(word_list):
 nhands=int(raw_input("Enter total number of hands: "))
 totalScore=0
 for i in range(nhands):
  hand=deal_hand(7,True)
  #if(i==0):hand=get_frequency_dict("aci*prt")
  #else:hand=get_frequency_dict("dd*lout")

  print "current hand:", display_hand(hand)
  ans=raw_input("Would you like to substitute a letter? ")
  if(ans=="yes"):
     letter=raw_input("Which letter would you like to replace: ")
     hand=substitute_hand(hand,letter)
     #hand=get_frequency_dict("dd*aout")
  internalScore=play_hand(hand, word_list)
  ans=raw_input("Would you like to replay the hand? ")
  if(ans=="yes"): 
   internalScore=play_hand(hand, word_list)
  totalScore+=internalScore 
 print "Total score over all hands: ",totalScore  
 return totalScore  

word_list=load_words()
play_game(word_list)

#hand=get_frequency_dict("dd*aout") 
#play_hand(hand,word_list)

    






