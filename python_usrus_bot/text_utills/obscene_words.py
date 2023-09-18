def obscene_words_count(text: [str]) -> int:
    count = 0
    for word in text:
        if word.lower() in obscene_words:
            count += 1
    return count


obscene_words: set[str] = {

}
