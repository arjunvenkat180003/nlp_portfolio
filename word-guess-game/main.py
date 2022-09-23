from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import sys
from random import seed
from random import randint
seed(1234)

def preprocess(tokens):

    #turn lowercase
    tokens = [t.lower() for t in tokens]
    # get rid of punctuation and stopwords
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
    #only length > 5
    tokens = [t for t in tokens if len(t) >=5]

    wnl = WordNetLemmatizer()

    lemmas = [wnl.lemmatize(t) for t in tokens]

    lemmas = set(lemmas)

    tags = pos_tag(lemmas)

    #print(tags)

    noun_lemmas = [tag[0] for tag in tags if tag[1] == 'NN']

    print("Number of tokens: "+str(len(tokens)))

    print("Number of nouns: "+str(len(noun_lemmas)))

    #print(noun_lemmas)

    #print(tokens)

    return (tokens, noun_lemmas)


def create_dict(tokens, nouns):
    
    noun_counts = {}

    nouns = set(nouns)

    for token in tokens:
        if token in nouns:
            if token in noun_counts:
                noun_counts[token] += 1
            else:
                noun_counts[token] = 1
    
    #print(noun_counts)

    return noun_counts


def find_most_freq_words(filename):
    with open(filename) as txt_file:
        content = txt_file.read()
        #print(content)

        tokens = word_tokenize(content)

        unique_tokens = set(tokens)

        lexical_diversity = len(unique_tokens)/(float(len(tokens)))

        print("\nLexical diversity: %.2f" %lexical_diversity)

        tokens, nouns = preprocess(tokens)

        noun_counts = create_dict(tokens, nouns)

        sorted_counts = sorted(noun_counts.items(), key=lambda x: x[1], reverse=True)

        most_freq_words = []

        for i in range(50):
            most_freq_words.append(sorted_counts[i][0])
            print(sorted_counts[i])
        
        return most_freq_words

def guessing_game(most_freq_words):
    points = 5

    rand_ind = randint(0, 49)

    rand_word = most_freq_words[rand_ind]
    
    letter_guess = ' '
    cur_word = ''

    for i in range(len(rand_word)):
        cur_word += '_'
    
    user_won = False

    while points > 0 and letter_guess != '!' and not user_won:
        print("Word: "+cur_word)
        print("Current score "+str(points))

        letter_guess = input('Guess a letter ')

        if letter_guess in rand_word:
            print("Right!")
            points += 1

            temp_list = list(cur_word)
            for ind, letter in enumerate(rand_word):
                if letter == letter_guess:
                    temp_list[ind] = letter
            
            cur_word = "".join(temp_list)

            if '_' not in cur_word:
                print("Congratulations, you won!")


        else:
            print("Sorry guess again")
            points -= 1
    
    if not user_won:
        print("Sorry, you lost!")

    print("The word is: "+rand_word)
    print("User score: "+str(points))


#check if argument is correct, exit otherwise
if len(sys.argv) != 2:
    print('Error, need an argument')
    exit()


most_freq_words = find_most_freq_words(sys.argv[1])

guessing_game(most_freq_words)




    


