import os, json, re

load_file = Core.storage.load

class JsonTVShowsAfent(Agent.TV_Shows):

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
        for season in media.children:
            self.updateSeason(metadata, season, lang)
    
    def updateSeason(self, metadata, media, lang):
        for episode in media.children:
            self.updateEpisode(metadata, episode, lang)

    def updateEpisode(self, metadata, media, lang):
        log.debug(media.items[0].parts[0].file)

        title, season, episode, directory = getShowSeasonAndEpisodeFromPath(media.items[0].parts[0].file)

        log.debug(title)
        log.debug(season)
        log.debug(episode)
        log.debug(directory)
        log.debug(os.path.exists(os.path.join(directory, "Info.json")))


# Help function

def getShowSeasonAndEpisodeFromPath(path):
    file = os.path.basename(path)
    title = season = episode = directory = ""


    if re.search("^(e|E){0,1}[0-9]{1,}\.[^.]*$", file):
        episode = (file[1:] if re.search("^(e|E)", file) else file).split('.')[0]

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

    return title, season, episode, directory


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