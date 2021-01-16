import random
import string
import pylab

WORDLIST_FILENAME = "words.txt"


def load_words():
  print("Loading word list from file...")
  inFile = open(WORDLIST_FILENAME, 'r')
  line = inFile.readline()
  wordlist = line.split()
  print len(wordlist), "words loaded."
  return wordlist

def choose_word(wordlist):
  return random.choice(wordlist)

def is_word_guessed(secret_word, letters_guessed):
 #returns a boolean according to the guess 
 secret_word=secret_word.lower()
 letters_guessed=[ch.lower() for ch in letters_guessed]     
 cont=0
 for ch in secret_word:
  if (ch in letters_guessed): cont+=1
 if(cont==len(secret_word)): return True
 else:return False 

def get_guessed_word(secret_word, letters_guessed):
 # returns guessed word in the format __xx__x. letters_guessed is a list of chars'''
 secret_word=secret_word.lower()
 letters_guessed=[ch.lower() for ch in letters_guessed]
 guess=["_"]*len(secret_word)
 for i in range(len(secret_word)):
  if (secret_word[i] in letters_guessed): guess[i]=secret_word[i]
 s=""
 for e in guess:
  s+=str(e)
 return s

def get_available_letters(letters_guessed):
 #returns the letters available in the alphabet 
 alpha=string.ascii_lowercase
 for ch in letters_guessed:
  alpha=alpha.replace(ch,"")
 return alpha

def hangman(secret_word):
 print "Welcome to the game Hangman!"
 print "I am thinking of a word that is "+str(len(secret_word))+" letters long."
 print "You have 3 warnings left. ", "\n","------------"  
 limit=6  #limit of guesses
 warn=3   #limit of warnings
 count=0
 letters_guessed=[]
 total=0  #total score
 while(True):
  print "You have "+str(limit)+" guesses left."
  if(count==0): print "Available letters: "+string.ascii_lowercase
  else: print "Available letters: "+str(get_available_letters(letters_guessed))
  ch=raw_input("Please guess a letter: ")
  ch=ch.lower()
  count+=1

  if(len(ch)!=1):    #if we guess a word instead of a char
   if(ch==secret_word):
    print "Congratulations, you won!"
    print "Your total score for this game is:",total
    break
   else:
    limit-=1  
    print "Oops we guessed the wrong word","\n","----------"
  else:
    if(ch=="*"):    #if we are skying for a help
      myword=get_guessed_word(secret_word, letters_guessed)
      matches=pylab.array(show_possible_matches(myword))
      print "Possible word matches are:","\n", matches
    else:          #if we are plying with chars  
      if(ch.isalpha()):
       if(ch in letters_guessed): 
        warn-=1
        if(warn<0): 
         limit-=1
         print "Oops! You've already guessed that letter. You have no warnings left \
                so you lose one guess: ", guess,"\n","------------"
        else:
         print "Oops! You've already guessed that letter. You have "+str(warn)+" warnings left "
         print guess, "\n","------------" 
       else:     #we play with an allow character of the alphabet
        letters_guessed.append(ch)
        guess=get_guessed_word(secret_word, letters_guessed)
        total+=1
        if(ch in secret_word): print "Good guess:", guess,"\n","------------" 
        else:
         if(ch in "aeiou"):limit-=2
         else: limit-=1 
         print "Oops! That letter is not in my word: "
         print "Please guess a letter: ",guess,"\n","------------" 
      else:
       warn-=1
       total+=1
       if(warn<0):
        limit-=1
        print "Oops! That is not a valid letter. You have no warnings left \
                so you lose one guess", guess,"\n","------------"
       else:
        print "Oops! That is not a valid letter. You have "+str(warn)+\
             " warnings left: "+guess+"\n","------------" 
  if(is_word_guessed(secret_word, letters_guessed)): 
   print "Congratulations, you won!"
   print "Your total score for this game is:",total
   break 
  if(limit<=0):
   print "you lost", "the word was:",secret_word 
   break 

def match_with_gaps(myword, other_word):
  def isRepeated(word,ch):
   nmatches=0
   for e in word:
    if(e==ch):nmatches+=1
   if(nmatches>1): return True
   else: return False 

  if(len(myword)!=len(other_word)): return False
  for i in range(len(myword)):
     if(myword[i]!="_"):
      if(myword[i]!=other_word[i]): return False 
      if(isRepeated(other_word,myword[i]) and not isRepeated(myword,myword[i])): return False
  return True


def show_possible_matches(myword):
 matches=[]
 for word in wordlist:
  if(match_with_gaps(myword,word)):
   matches.append(word)
 if(len(matches)==0): print "no matches"
 return matches   

wordlist=load_words()
secret_word=choose_word(wordlist)
#secret_word="else"
hangman(secret_word)




















