def kolla_palindrom():
    word = input("Word: ")
    word_reversed = '' .join(reversed(word))
    if word.lower() == word_reversed.lower():
        print("Is palindrome")
    else:
        print ("Not palindrome")

kolla_palindrom()