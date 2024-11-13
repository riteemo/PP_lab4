from yandex_music import ClientAsync
from random import choice

# Класс для работы с API Яндекс Музыки
class YandexMusicAPI:
    def __init__(self, token: str):
        self.__client = ClientAsync(token)

    async def initialize(self):
        await self.__client.init()

    # Рейтинг песен
    async def get_chart(self) -> str:
        CHART_ID = 'world'
        chart = (await self.__client.chart(CHART_ID)).chart
        text = [f'🏆 {chart.title}', chart.description, '', 'Треки:']

        for track_short in chart.tracks:
            track, chart = track_short.track, track_short.chart
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)

            track_text = f'{track.title}{artists}'

            if chart.progress == 'down':
                track_text = '🔻 ' + track_text
            elif chart.progress == 'up':
                track_text = '🔺 ' + track_text
            elif chart.progress == 'new':
                track_text = '🆕 ' + track_text
            elif chart.position == 1:
                track_text = '👑 ' + track_text

            track_text = f'{chart.position} {track_text}'
            text.append(track_text)

        return '\n'.join(text)

    # Рейтинг песен артиста
    async def get_chart_by_artist(self, artist_name: str) -> str:
        print(artist_name)
        try:
            query_res = await self.__client.search(artist_name)
            best_artists_name = query_res.best['result']['name'] # лучшее совпадение по имени
            best_artist_id = query_res.best['result']['id']
            result_arr = [f"Топ 10 песен по исполнителю {best_artists_name}"]
            songs = await self.__client.artistsTracks(best_artist_id)
            for track in range(1, 11):
                result_arr.append(f"{track} - {songs[track - 1]['title']}")
            return "\n".join(result_arr)
        except Exception as E:
            print(E)
            return ''

    # Рандомная песня артиста
    async def get_random_song(self, artist_name: str) -> str:
        print(artist_name)
        try:
            query_res = await self.__client.search(artist_name)
            best_artist_id = query_res.best['result']['id']
            best_artist_name = query_res.best['result']['name']
            result_arr = [f"Случайная песня исполнителя {best_artist_name} —"]
            song = choice(await self.__client.artistsTracks(best_artist_id))
            result_arr.append(song['title'])
            print(result_arr)
            return " ".join(result_arr)
        except Exception as E:
            print(E)
            return ''