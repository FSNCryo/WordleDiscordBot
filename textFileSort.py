import json

# Opening JSON file
w = ":regional_indicator_w:"
for length in range(5, 13):
    with open('../WordleDiscordBotOld/clean_words.txt') as words_file:
        word = words_file.readline()
        word_List = {}
        while word:
            if len(word)-1 == length:
                word_List[(word.strip("\n"))] = len(word)-1
            word = words_file.readline()
        words_file.close()

        with open('Game/words.json', 'a+') as json_file:
            word = {length: [word_List]}
            print(json.dump(word, json_file, indent=4))

        json_file.close()

