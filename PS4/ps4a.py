
def get_permutations(sequence,sofar="",result=[]):
   '''Enumerate all permutations of a given string'''
   if(sequence==""): result.append(sofar)
   for i in range(len(sequence)):
    next=sofar+sequence[i]
    remaining=sequence[0:i]+sequence[i+1:]
    get_permutations(remaining,next)
    
   return result
 

