from itertools import islice
import numpy as np
import re

class Game: 
    '''Определите название, правила игры, метод подготоовки к ней и сборка игры в коробку
    Все данные вводятся в строковом формате, при этом жанр должен относится к следующим:
    'фэнтези', 'приключение', 'детектив', 'головоломка', 'азартные' '''

    genres = ['фэнтези', 'приключение', 'детектив', 'головоломка', 'азартные']
    
    def __init__(self, name, rules, prep_method, pack_method, genre):
        self.name = name
        self.rules = rules
        self.prep_method = prep_method
        self.pack_method = pack_method
        self.genre = genre
        self.verify_genres(genre)

    @classmethod
    def verify_genres(cls, genre_pref):
         if genre_pref.lower() not in cls.genres:
            raise TypeError(f'Неверно введены жанры игры. Убедитесь, что данные введены в формате списка и названия соответствуют перечисленным {cls.genres}')
            


class Professor():
    '''Назовите имя профессора, предпочитаемые им жанры в виде списка и предпочтительную
    продолжительность партии в часах в виде диапазона ('1-2') или числа'''
    genres = Game.genres
   
    def __init__(self, name, genre_pref, dur_pref):
        self.name = name
        self.genre_pref = genre_pref
        self.dur_pref = self.transform_dur(dur_pref)
        self.verify_genres(genre_pref)
        
    @classmethod
    def verify_genres(cls, genre_pref):
         if not any(genre.lower() in genre_pref for genre in cls.genres) or type(genre_pref) != list:
            raise TypeError(f'Неверно введены жанры игры. Убедитесь, что данные введены в формате списка и названия соответствуют перечисленным {cls.genres}')
            
    @classmethod
    def verify_dur(cls, dur_pref):
        if bool(re.match("\d+-\d+", dur_pref)) == False and dur_pref.isnumeric() == False:
            raise TypeError('Введите диапазон предпочтительной длительности партии в часах в формате "число-число", пример "1-2"')

    def transform_dur(self, dur_pref):
        self.verify_dur(dur_pref)
        if dur_pref.isnumeric():
            return [float(dur_pref)]
        else:
            range = [float(i) for i in dur_pref.split('-')]
            return list(np.arange(float(range[0]), float(range[1] + 1)))



class MultiplayerGame(Game):
    '''Определите игру на несколько игроков
    Дополнительно можно ввести минимальное и максимальное число игроков, а так же среднюю продолжительность игровой партии
    в часах.
    В данном классе представлены методы проверки возможности начала игры по заданному списку преподавателей'''
    
    min_players = 2
    max_players = 6
    dur = 1

    def verify_professors(self, professors: list):
        if type(professors[0]) != Professor:
            raise TypeError('Элементы списка преподавателей имеют неправильный тип данных, используйте функцию ReadFile.read_file("Professor", file_path)')

    def verify_num_attr(self, min_players, max_players, dur):
        if type(min_players) not in [int, float] or (type(max_players) not in [int, float]) or (type(dur) not in [int, float]):
            raise TypeError('Убедитесь, что в поля min_players и max_players введены числа') 
        
    def enough_players(self, professors: list):
        self.verify_num_attr(self.min_players, self.max_players, self.dur)
        if self.min_players <= len(professors) <= self.max_players:
            return True
        return False
        
    def agree_on_genres(self, professors: list):
        for prof in professors:
            if self.genre not in prof.genre_pref:
                return False
        return True
    
    def agree_on_dur(self, professors: list):
        self.verify_num_attr(self.min_players, self.max_players, self.dur)
        for prof in professors:
            if self.dur not in prof.dur_pref:
                return False
        return True
    
    def passes_all_crits(self, professors: list):
        self.verify_num_attr(self.min_players, self.max_players, self.dur)
        if self.enough_players(professors, self.min_players, self.max_players) and self.agree_on_genres(professors) and self.agree_on_dur(professors):
            return True
        return False



class GameRoom(MultiplayerGame):
    '''Игровая комната кафедры философии: список игр, список преподавателей, 
    метод подбора игры для заданного подмножества преподавателей'''

    def __init__(self, games: list, professors: list):
        self.games = games
        self.professors = professors
        self.choose_a_game(games, professors)

    def choose_a_game(self, games, professors):
        sorted_games = {}

        for game in games:
                if self.enough_players(professors):
                    if game.agree_on_genres(professors) and game.agree_on_dur(professors): 
                         sorted_games[game.name] = 1
                    elif game.agree_on_genres(professors) and game.agree_on_dur(professors) == False: 
                         sorted_games[game.name] = 2
                    elif game.agree_on_genres(professors) == False and game.agree_on_dur(professors): 
                         sorted_games[game.name] = 3
                    elif game.agree_on_genres(professors) == False and game.agree_on_dur(professors) == False: 
                         sorted_games[game.name] = 3
        
        if sorted_games != {}:
          sorted_games = dict(sorted(sorted_games.items(), key=lambda x:x[1]))

          mes_dict = {1: 'Игра полностью подходит вашей компании!', 2: 'Игра соответсвует вашим предпочтениям в жанрах, но не всем подойдет по длительности',
                         3: 'Игра подойдет вам по длительности, но может не подойти по жанру',
                         4: 'Игра не подойдет вам ни по жанру, ни по длительности, но может быть интересна'}
          print(f'Список игр, в которые вы можете сыграть:')
        
          for game in sorted_games:
               print('')
               print(f'{sorted_games[game]}. {game} - {mes_dict[sorted_games[game]]}')
               print('')
               print('------------------------')

        else: print('Число игроков превышает допустимое')



class ReadFile():
    '''В данном классе представлены методы для считывания представленной в текстовом файле
    информации об играх и профессорах.
    В качестве разделителей в файлах используется ';' '''
    name_class_dict = {'Game': Game, 'Professor': Professor, 'MultiplayerGame': MultiplayerGame}

    def __init__(self, class_name, file_path):
        self.class_name = class_name
        self.file_path = file_path
        self.item_list = self.read_file(class_name, file_path)

    def read_file(self, class_name, file_path):
        item_list = []
        
        with open(file_path, "r", encoding='UTF-8') as f:
            for lines in islice(f, 1, None):
                add_info = []
                attr = []
                l = len(lines.split(';'))
                line = lines.strip('\n').replace(' ', '').split(';')

                if class_name == 'MultiplayerGame':
                    attr = [lines.split(';')[0]] + line[1:5]
                    if l > 5:
                        add_info = line[5:l]

                if class_name.capitalize() == 'Professor':
                    attr = [line[0], line[1].split(','), line[2]]

                if class_name.capitalize() == 'Game':
                    attr = [lines.split(';')[0]] + line[1:l]

                else: TypeError('Неправильно введено название класса, введите одно из следующих: Professor, Game, MultiplayerGame')
                
                item_list.append(self.name_class_dict[class_name](*attr))

                if add_info != []:
                    item_list[len(item_list)-1].min_players = int(add_info[0])
                    item_list[len(item_list)-1].max_players = int(add_info[1])
                    item_list[len(item_list)-1].dur = int(add_info[2])

        return item_list