import csv
import requests


def words_filter(anime, category, chose):
    newanime = []
    for one_anime in anime:
        flag = 1
        for j in chose:
            if int(one_anime[category].split(', ').count(j)) != 1:
                flag = 0
        if flag != 0:
            newanime.append(one_anime)
    return newanime


def numbers_filter(anime, category, chose):
    newanime = []
    for one_anime in anime:
        if one_anime[category] != 'Unknown':
            if float(one_anime[category]) >= float(chose[0]):
                newanime.append(one_anime)
    return newanime


def save(your_anime):
    with open('your_anime.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Anime-PlanetID', 'Name', 'Alternative Name', 'Rating Score', 'Number Votes', 'Tags', 'Content Warning', 'Type', 'Episodes', 'Finished', 'Duration', 'StartYear', 'EndYear', 'Season', 'Studios', 'Synopsis', 'Url'))
        for one_anime in your_anime:
            writer.writerow((one_anime['Anime-PlanetID'], one_anime['Name'], one_anime['Alternative Name'], one_anime['Rating Score'], one_anime['Number Votes'], one_anime['Tags'], one_anime['Content Warning'], one_anime['Type'], one_anime['Episodes'], one_anime['Finished'], one_anime['Duration'], one_anime['StartYear'], one_anime['EndYear'], one_anime['Season'], one_anime['Studios'], one_anime['Synopsis'], one_anime['Url']))
    f.close()


anime = list(dict())
with open('anime.csv', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for one_anime in reader:
        anime.append(one_anime)
f.close()

your_anime = anime

category = 'Type'
print('Какой тип аниме вас интересует?')
chose = input()
chose = chose.split(', ')
if chose != ['']:
    your_anime = words_filter(your_anime, category, chose)

category = 'Finished'
print('Вы хотите аниме было завершено?')
chose = input()
if chose:
    if chose == 'Да' or chose == 'да':
        chose = ['True']
    else:
        chose = ['False']
    if chose != ['']:
        your_anime = words_filter(your_anime, category, chose)

category = 'Studios'
print('Аниме какой студии вы хотите посмотреть?')
chose = input()
chose = chose.split(', ')
if chose != ['']:
    your_anime = words_filter(your_anime, category, chose)

category = 'Tags'
print('Какие тэги в описании аниме должны присутствовать(перечислите через запятую)?')
chose = input()
chose = chose.split(', ')
if chose != ['']:
    your_anime = words_filter(your_anime, category, chose)

category = 'Rating Score'
print('Какой минимальный рейтинг должен быть у аниме?')
chose = input()
chose = chose.split(', ')
if chose != ['']:
    your_anime = numbers_filter(your_anime, category, chose)
save(your_anime)

if len(your_anime) > 5:
    number_of_posters = 5
else:
    number_of_posters = len(your_anime)
for i in range(number_of_posters):
    poster = requests.get('https://www.anime-planet.com/images/anime/covers/thumbs/' + your_anime[i]['Anime-PlanetID'] + '.jpg')
    if i == 0:
        file = open('Poster1.jpg', 'wb')
    elif i == 1:
        file = open('Poster2.jpg', 'wb')
    elif i == 2:
        file = open('Poster3.jpg', 'wb')
    elif i == 3:
        file = open('Poster4.jpg', 'wb')
    elif i == 4:
        file = open('Poster5.jpg', 'wb')
    file.write(poster.content)
    file.close()
print('Список подходящих вам аниме находятся в файле your_anime.csv, также сохранены постеры к первым 5 аниме')

