def count_words(sentence):
    words = sentence.split()
    word_count = {}
    
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    return word_count

sentence = input("Enter a sentence: ")
result = count_words(sentence)
print(result)