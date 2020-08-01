def isbn_or_key(word):
    key_or_isbn = "key"
    if len(word) == 13 and word.isdigit():
        key_or_isbn = "isbn"
    new_word = word.replace("-", "")
    if "-" in word and len(new_word) == 10 and new_word.isdigit():
        key_or_isbn = "isbn"
    return key_or_isbn
