"""
Nicholas Graham
Caesar Shift function for Algorithms and Data Structures
Slightly overcomplicated and way overdue, but it works pretty well
NLTK is required for the cracking algorithm, but everything else can run without it
"""
canMultiprocess = True
try:
    import multiprocessing as mp
except ImportError:
    canMultiprocess = False
    print("Multiprocessing unavailable")
    
canSpellCheck = True
try:
    import nltk
    nltk.download('words')
    from nltk.corpus import wordnet
except ImportError:
    canSpellCheck = False


class CipherCracking:
    
    def __init__(self):
        
        self.sensitivity = 0.5
        
        self.english_words  = set(w.lower() for w in nltk.corpus.words.words())

    def threadedCrack(self, shift):
        # This is the function that actually decodes the item, the reason its in a class
        # Is because I didn't know what a starmap was and don't want to rewrite my
        # Code to work with it
        # It just calls the decode function and tells it not not multithread it
        item = decode(self.string, shift, True)
        found = [1 for i in item.split(" ") if i in self.english_words]
        if len(found) >= len(item.split(" "))*self.sensitivity:
            return [item, shift, len(found)]
        else:
            return [None, -1, -1]
        print("I broke")
        

    def crack(self, string, shift):
        string = string.lower()
        result = []
        if canMultiprocess:
            # This is the multithreaded aspect
            lst = range(26)
            self.string = string
            with mp.Pool() as pool:
                # We pool all the items and map them to the function
                items = pool.map(self.threadedCrack, lst)
            highest = -2
            highest_word = None
            # This loops through and looks for all the valid finds
            for v in items:
                if v[0] != None:
                    if v[2] > highest:
                        highest = v[2]
                        highest_word = (v[0], v[1])
                    result.append(f'Found "{v[0]}" with key of {v[1]}')
            # Figures out what one is most likely (based on most correct words)
            if highest_word:
                result.append(f'Most likely is "{highest_word[0]}" with key {highest_word[1]}')
        else:
            # For the nerds that can't multithread heres the implementation
            for i in range(26):
                item = self.threadedCrack(i)
                if item[0] != None:
                    result.append(f'Found "{v[0]}" with key of {v[1]}')
            result.append(f'Most likely is "{highest_word[0]}" with key {highest_word[1]}')
                
                
        if result == []:
            result.append("No items were found")
        return "\n".join(result)
            
        
def shift_func(string, shift):
    # normally I'd use list comprehension to solve this, but I don't know if you'd classify it as a loop
    result = []
    for i in [*string]:
        # I had a better way to do this. I forgot it
        # This takes the basic shift
        shifted = ord(i)+shift
        while shifted > 122:
            # If the letter is greater then z, wrap it back around
            shifted -= 26
        while shifted < 97:
            # Wrap it around if its less then a
            shifted += 26
        # return the letter, but as a letter
        result.append(chr(shifted))
    #Put the letters together and return it
    return "".join(result)

def encode(string, shift, overrideMultiprocess=False):
    # Encodes the shift
    capital_indexes = [i for i, v in enumerate(string) if v.isupper()]
    split_string = [i.lower() for i in string.split(" ")]
    if canMultiprocess and not overrideMultiprocess:
        with mp.Pool(5) as pool:
            result = pool.starmap(shift_func, [(i, shift) for i in split_string])
    else:
        result = []
        for i in string.split(" "):
            result.append(shift_func(i, shift))
        
    result = " ".join(result)
    for i in capital_indexes:
        result = "".join(["".join(result[0:i]), result[i].upper(), "".join(result[i+1:])])
    return result

def decode(string, shift, overrideMultiprocess=False):
    # Decodes a shifted string
    return encode(string, shift*-1, overrideMultiprocess)




def gatherInput():
    "Grabs the input"
    entry = input("What do you want to run? (Encode, Decode, Crack): ").lower() # Really the only one that matters is the first letter
    if len(entry) > 0:
        entry = entry[0]
    else:
        print("--INVALID INPUT--")
        return gatherInput()
    if entry != "c":
        func_obj = None
        if entry == "e":
            func_obj = encode
        elif entry == "d":
            func_obj = decode
        else:
            # Catch invalid reads
            print("--INVALID INPUT--")
            return gatherInput()
    
        string = input("What string do you want to encode/decode: ")
        shift = input("What is the shift: ")
        if shift.isnumeric():
            shift = int(shift)
        else:
            print("shift is not an integer")
            return gatherInput()
        return func_obj, string, shift%26
    else:
        
        if not canSpellCheck: # This is only required for the cracking function
            quit("Please install nltk module (pip install nltk)")
        
        string = input("What is the encrypted string (outputs will be lowercase): ")
        
        #prep the cracker
        cracker = CipherCracking()
        return cracker.crack, string, None

def main():
    # gathers the inputs
    func, string, shift, = gatherInput()
    #adds space for readability
    print("\n"*3)
    #Runs whatever function was returned
    result = func(string, shift)
    print(result)
    
if __name__ == "__main__":
    main()