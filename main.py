import json

totalIter = 0
MORSE_TRANSL = {'.-': 'A', '-...': 'B', '-.-.': 'C',
             '-..': 'D', '.': 'E', '..-.': 'F',
             '--.': 'G', '....': 'H', '..': 'I',
             '.---': 'J', '-.-': 'K', '.-..': 'L',
             '--': 'M', '-.': 'N', '---': 'O',
             '.--.': 'P', '--.-': 'Q', '.-.': 'R',
             '...': 'S', '-': 'T', '..-': 'U',
             '...-': 'V', '.--': 'W', '-..-': 'X',
             '-.--': 'Y', '--..': 'Z'}
IS_CONSONANT = {'A': False, 'B': True,
         'C': True, 'D': True, 'E': False,
         'F': True, 'G': True, 'H': True,
         'I': False, 'J': True, 'K': True,
         'L': True, 'M': True, 'N': True,
         'O': False, 'P': True, 'Q': True,
         'R': True, 'S': True, 'T': True,
         'U': False, 'V': True, 'W': True,
         'X': True, 'Y': True, 'Z': True}


def codebreaker(currentCode, currentPhrase, currentSentence, index, addWord):

    # Check if valid English word
    if wordDict.get(currentPhrase) == 0 and addWord:

        # Iterate, keeping adding letters without creating a word
        codebreaker(currentCode, currentPhrase, currentSentence, index, False)

        # Continue, create a word
        currentSentence += currentPhrase + ' '
        currentPhrase = ''

    if len(symbolList) > index > -1:
        currentCode += symbolList[index]

        if currentCode in MORSE_TRANSL:
            cp = len(currentPhrase) - 1

            # If a word has more than 2 vowels or 3 consonants in a row, scrap it and start a new combo
            if cp > 3:
                if all(IS_CONSONANT[currentPhrase[cp - i]] for i in range(3)):
                    index = -2
                if all(not IS_CONSONANT[currentPhrase[cp - i]] for i in range(2)):
                    index = -2

            # Continue string of morse code
            codebreaker(currentCode, currentPhrase, currentSentence, index + 1, True)

            currentPhrase += MORSE_TRANSL[currentCode]
            # Break string of morse code, start a new character
            codebreaker('', currentPhrase, currentSentence,  index + 1, True)

        else:
            # If string of morse code is not legible, back track and count as a character
            currentPhrase += MORSE_TRANSL[currentCode[:-1]]
            codebreaker('', currentPhrase, currentSentence, index, True)

    else:
        # Add to total iteration once string is complete or trashed
        global totalIter
        totalIter += 1

        # if the string is a complete combination of words, add to a set of every phrase
        if currentCode == '' and currentPhrase == '' and index > -1:
            if currentSentence not in allPhrases:
                allPhrases.add(currentSentence)


# Return total words in sentence
def sortKey(s):
    return len(s.split())


# Display results of program
def displayResults():
    phraseList = list(allPhrases)
    sortedPhrases = sorted(phraseList, key=sortKey)
    i = 0
    print('Possible phrases (from most to least likely):')
    for phrase in sortedPhrases:
        i += 1
        print(f'{i} - {phrase}')
    print('')
    print(f'Total iterations: {totalIter}')


if __name__ == '__main__':

    # Input code here - NOTE: Input must be short, long inputs mean exponentially long run times
    code = '....-.-..-..--.-.----...' # Test 1 - Code: SECRET CODE
    # code = '-....-.-..-.-..'  # Test 2 - Code: BE KIND
    # code = '.-..---...-.-.-..---.-.....'  # Test 3 - Code: LOVE CATCH
    # code = '-.....-..-.--......-...-.--.'  # Test 4 - Code: NEVER GIVE UP

    symbolList = list(code)

    # Open dictionary with 1000 most common words
    f = open('common.json')
    wordDict = json.load(f)

    allPhrases = set()

    # Start recursive process
    print("Starting recursive search, please be patient...")
    codebreaker('', '', '', 0, True)

    # Display results
    displayResults()

