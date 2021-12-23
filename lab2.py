import csv
import requests

FILE_ANIME = 'anime.csv'
TOP_SIZE = 5

questions = {
    'Type': 'Какой тип аниме вас интересует?',
    'Finished': 'Вы хотите аниме было завершено?',
    'Studios': 'Аниме какой студии вы хотите посмотреть?',
    'Tags': 'Какие тэги в описании аниме должны присутствовать(перечислите через запятую)?',
    'Rating Score': 'Какой минимальный рейтинг должен быть у аниме?'
}


def open_file(FILE_ANIME):
    your_anime = list(dict())
    with open(FILE_ANIME, encoding='utf8') as f:
        reader = csv.DictReader(f)
        for one_anime in reader:
            your_anime.append(one_anime)
    f.close()
    return your_anime


def words_filter(anime, category, chose):
    newanime = []
    for one_anime in anime:
        chose_in_anime = True
        for one_chose in chose:
            if int(one_anime[category].split(', ').count(one_chose)) != 1:
                chose_in_anime = False
        if chose_in_anime == True:
            newanime.append(one_anime)
    return newanime


def numbers_filter(anime, category, chose):
    newanime = []
    for one_anime in anime:
        if one_anime[category] != 'Unknown':
            if float(one_anime[category]) >= float(chose[0]):
                newanime.append(one_anime)
    return newanime


def save_anime(your_anime):
    with open('your_anime.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Anime-PlanetID', 'Name', 'Alternative Name', 'Rating Score', 'Number Votes', 'Tags',
                         'Content Warning', 'Type', 'Episodes', 'Finished', 'Duration', 'StartYear', 'EndYear',
                         'Season', 'Studios', 'Synopsis', 'Url'))
        for one_anime in your_anime:
            writer.writerow((one_anime['Anime-PlanetID'], one_anime['Name'], one_anime['Alternative Name'],
                             one_anime['Rating Score'], one_anime['Number Votes'], one_anime['Tags'],
                             one_anime['Content Warning'], one_anime['Type'], one_anime['Episodes'],
                             one_anime['Finished'], one_anime['Duration'], one_anime['StartYear'], one_anime['EndYear'],
                             one_anime['Season'], one_anime['Studios'], one_anime['Synopsis'], one_anime['Url']))
    f.close()


def save_posters(your_anime):
    if len(your_anime) > TOP_SIZE:
        number_of_posters = TOP_SIZE
    else:
        number_of_posters = len(your_anime)
    for i in range(number_of_posters):
        poster = requests.get(
            'https://www.anime-planet.com/images/anime/covers/thumbs/' + your_anime[i]['Anime-PlanetID'] + '.jpg')
        file = open(f'Poster{i + 1}.jpg', 'wb')
        file.write(poster.content)
        file.close()


your_anime = open_file(FILE_ANIME)

for category, question in questions.items():
    print(question)
    chose = input()
    chose = chose.split(', ')
    if category == 'Type':
        if chose != ['']:
            your_anime = words_filter(your_anime, category, chose)
    elif category == 'Finished':
        chose = chose[0]
        chose = ['True'] if chose.lower() == 'да' else ['False']
        if chose != ['']:
            your_anime = words_filter(your_anime, category, chose)
    elif category == 'Studios':
        if chose != ['']:
            your_anime = words_filter(your_anime, category, chose)
    elif category == 'Tags':
        if chose != ['']:
            your_anime = words_filter(your_anime, category, chose)
    elif category == 'Rating Score':
        if chose != ['']:
            your_anime = numbers_filter(your_anime, category, chose)

save_anime(your_anime)
save_posters(your_anime)

print('Список подходящих вам аниме находятся в файле your_anime.csv, также сохранены постеры к первым 5 аниме')
