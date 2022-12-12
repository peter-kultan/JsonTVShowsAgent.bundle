import os, json, re
from dateutil.parser import parse

load_file = Core.storage.load
MediaProxy = Proxy.Media

class JsonTVShowsAgent(Agent.TV_Shows):

    name = 'JsonTVShowsAgent'
    primary_provider = True

    persist_stored_files = False

    languages = [Locale.Language.NoLanguage]
    accepts_from = [
        'com.plexapp.agents.localmedia',
        'com.plexapp.agents.opensubtitles',
        'com.plexapp.agents.podnapisi',
        'com.plexapp.agents.plexthememusic',
        'com.plexapp.agents.subzero'
        ]

    contributes_to = [
        'com.plexapp.agents.thetvdb'
        ]

    def search(self, results, media, lang):
        log.debug(media.show)
        log.debug(media.season)
        log.debug(media.episode)
        log.debug(media.name)

        results.Append(MetadataSearchResult(id=media.id, name=media.show, lang=lang, score=100))

    def update(self, metadata, media, lang):
        dictionary, directory = get_episodes_from_show(media)

        path = os.path.join(directory, 'Info.json')

        if not os.path.exists(path):
            return

        info = json.loads(load_file(path))

        for show, seasons in dictionary.items():
            show_info = info[show]

            try: metadata.title = show_info['title']
            except: pass

            try: metadata.original_title = show_info['original_title']
            except: pass

            try: metadata.originally_available_at = parse(show_info['originally_available_at'])
            except: pass

            try: metadata.summary = show_info['summary']
            except: pass

            try: metadata.rating = show_info['rating']
            except: pass

            try: metadata.studio = show_info['studio']
            except: pass

            try: 
                poster_path = show_info['poster_path']
                poster = load_file(poster_path)
                metadata.posters[poster_path] = MediaProxy(poster)
            except: 
                pass

            metadata.genres.clear()

            try:
                for g in show_info['genres']:
                    metadata.genres.add(g)
            except:
                pass

            metadata.countries.clear()

            try:
                for d in show_info['countries']:
                    metadata.countries.add(d)
            except:
                pass

            self.update_seasons(metadata, seasons, show_info)


    def update_seasons(self, metadata, dictionary, info):
        for season, episodes in dictionary.items():
            try: 
                season_info = info['seasons'][str(season).zfill(2)]
                season_metadata = metadata.seasons[season]
            except: continue

            try: season_metadata.title = season_info['title']
            except: pass

            try: season_metadata.summary = season_info['summary']
            except: pass

            self.update_episodes(season_metadata, episodes, season_info)


    def update_episodes(self, metadata, episodes, info):
        for episode in episodes:
            try: 
                episode_info = info['episodes'][str(episode).zfill(2)]
                episode_metadata = metadata.episodes[episode]
            except:
                continue

            try: episode_metadata.title = episode_info['title']
            except: pass

            try: episode_metadata.originally_available_at = parse(episode_info['originally_available_at'])
            except: pass

            try: episode_metadata.summary = episode_info['summary']
            except: pass

            try: episode_metadata.rating = episode_info['rating']
            except: pass


# Help function


def get_episodes_from_show(media):
    dictionary = dict()

    for ch in media.children:
        if len(ch.items) > 0:
            directory = get_show_seasons_episodes_from_path(ch.items[0].parts[0].file, dictionary)
        else:
            dictionary, directory = get_episodes_from_show(ch)

    return dictionary, directory

def get_show_seasons_episodes_from_path(path, dictionary):
    file = os.path.basename(path)
    title = season = episode = directory = ""


    if re.search("^(e|E){0,1}[0-9]{1,}\.[^.]*$", file):
        episode = int((file[1:] if re.search("^(e|E)", file) else file).split('.')[0])

        dirpath = os.path.dirname(path)

        if re.search("^(s|S)[0-9]*$", os.path.basename(dirpath)):
            season = int(os.path.basename(dirpath)[1:])
        elif re.search("^[0-9]*$", os.path.basename(dirpath)):
            season = int(os.path.basename(dirpath))
        else:
            return None

        dirpath = os.path.dirname(dirpath)

        title = os.path.basename(dirpath)

        directory = os.path.dirname(dirpath)


    elif re.search("(s|S)[0-9]*(e|E)[0-9]*\.[^.]*$", file):
        res = re.search("^(.*) (s|S)([0-9]*)(e|E)([0-9]*)\.[^.]*$", file)
        title = res.group(1)
        season = int(res.group(3))
        episode = int(res.group(5))
        directory = os.path.dirname(path)

    if dictionary.get(title) is None:
        dictionary[title] = dict()

    if dictionary[title].get(season) is None:
        dictionary[title][season] = []

    dictionary[title][season].append(episode)

    return directory


class PlexLogAdapter(object):
    """
    Adapts Plex Log class to standard python logging style.
    This is a very simple remap of methods and does not provide
    full python standard logging functionality.
    """
    debug = Log.Debug
    info = Log.Info
    warn = Log.Warn
    error = Log.Error
    critical = Log.Critical
    exception = Log.Exception


class XBMCLogAdapter(PlexLogAdapter):
    """
    Plex Log adapter that only emits debug statements based on preferences.
    """
    @staticmethod
    def debug(*args, **kwargs):
        """
        Selective logging of debug message based on preference.
        """
        Log.Debug(*args, **kwargs)

log = XBMCLogAdapter