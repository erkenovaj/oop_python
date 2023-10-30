from all_classes import GameRoom, ReadFile

professors = ReadFile('Professor', 'data\profs.txt')
games = ReadFile('MultiplayerGame', 'data\multigames.txt')

GameRoom(games.item_list, professors.item_list)