import os
os.system("python count_freqs.py gene.train > gene.counts")
print("generating gene rare counts and train")

class Baseline:
    def __init__(self): #to be changed
        self.genecount = 0  #to be used for dev prediciton
        self.ocount = 0  #to be used for dev prediction
        self.wordDictionary = {} #keep track of all the words amount
        self.tupleDictionary = {} #keep track of count(appearances) + word
        self.trainDictionary = {} #keep track of word + symbol for rare
        self.rareword = [] #these words will be marked as _rare_
        self.Rare = '_RARE_'
        self.Owords = []
        self.Iwords = []
    
    #the goal of this method is to iterate through the "gene.counts" file
    #and collect all the information needed to manipulate
    def manipulate_gene(self, filename):
        data = [line.strip() for line in open(filename, 'r')]
        for word in data:
            #print(word)
            word = word.rstrip()
            #print(word)
            word = word.split(' ')
            #print(word[1])
            if word[1] == 'WORDTAG':
                location = word[3] #this is actually the word
                symbol = word[2] #this is the symbol that it comes with
                count = word[0] #this is the number of appearancs
                #print(location)
                if symbol == 'O':
                    tempo = int(count)
                    self.ocount += tempo
                    self.Owords.append(location)
                    if location in self.wordDictionary:
                        self.wordDictionary[location] += int(count)
                    else:
                        self.wordDictionary[location] = int(count)
                else:
                    tempi = int(count)
                    self.genecount += tempi
                    self.Iwords.append(location)
                    if location in self.wordDictionary:
                        self.wordDictionary[location] += int(count)
                    else:
                        self.wordDictionary[location] = int(count)
                #this is the all-word dictionary
                self.trainDictionary[location + ' ' + symbol] = int(count)
            else:
                #should never enter here
                print(word[1])
        print("done looping gene.count")
    
    #the goal of this is to replace all the rare words with _RARE_ but with care
    def gene_replace(self):
        gene_train = open('gene.train', 'r')
        new_train = open('gene-rare.train', 'w')
        #make it into the meat i want
        self.tupleDictionary = [(k, int(self.wordDictionary[k])) for k in self.wordDictionary]
        for tupleword in self.tupleDictionary:
            if int(tupleword[1]) < 5:
                self.rareword.append(tupleword[0])
        print("done collecting rarewords")
        for line in gene_train:
            #print(len(line.split(' ')))
            #print(line)
            length = len(line.split(' '))
            if length != 2:
                #print("entered")
                new_train.write(line)
                continue
            word = line.split(' ')[0]
            if word in self.Iwords:
                self.Iwords.remove(word)
            if word in self.Owords:
                self.Owords.remove(word)
            symbol = word
            if word in self.rareword:
                symbol = self.Rare
            toWrite = line.replace(word, symbol, 1)
            new_train.write(toWrite)
        new_train.close()
    
    #the goal of this method is to iterate through the gene-rare. counts and collect all the words
    # then update each value for emission
    def manipulate_rare(self, filename):
        data = [line.strip() for line in open(filename, 'r')]
        for word in data:
            word = word.rstrip()
            word = word.split(' ')
            #print(len(word))
            if word[1] == 'WORDTAG':
                location = word[3]
                symbol = word[2]
                count = word[0]
                if symbol == 'O':
                    self.ocount += int(count)
                else:
                    self.genecount += int(count)
                self.trainDictionary[location + ' ' + symbol] = int(count)

# here is to write the prediction out to the file
def generate_output(self):
    file = open('gene.dev', 'r')
    p1_out = open('gene_dev.p1.out', 'w')
    for w in file:
        if w != '\n':
            # from here on it's the emsission method
            w =  w.rstrip()
            s_O = w + ' ' + 'O'
                s_I = w + ' ' + 'I-GENE'
                num_O = 0
                num_I = 0
                if s_O in self.trainDictionary or s_I in self.trainDictionary:
                    if s_O in self.trainDictionary:
                        num_O = self.trainDictionary[s_O]
                    if s_I in self.trainDictionary:
                        num_I = self.trainDictionary[s_I]
            else:
                #print(w)
                k = self.Rare
                    s_O = k + ' ' + 'O'
                    s_I = k + ' ' + 'I-GENE'
                    if s_O in self.trainDictionary:
                        num_O = self.trainDictionary[s_O]
                if s_I in self.trainDictionary:
                    num_I = self.trainDictionary[s_I]
                O = float(num_O)/float(self.ocount)
                I = float(num_I)/float(self.genecount)
                if O > I:
                    p1_out.write(w + ' ' + 'O' + '\n')
    else:
        p1_out.write(w + ' ' + 'I-GENE' + '\n')
            else:
                p1_out.write(w)
    p1_out.close()

os.system("python count_freqs.py gene.train > gene.counts")
print("generating gene rare counts and train")
baseline = Baseline()
print("Baseline created and loading gene-counts")
baseline.manipulate_gene('gene.counts')
baseline.gene_replace()
print("done")

os.system("python count_freqs.py gene-rare.train > gene-rare.counts")
print("done")
baseline.manipulate_rare('gene-rare.counts')
baseline.generate_output()
os.system("python eval_gene_tagger.py gene.key gene_dev.p1.out")

