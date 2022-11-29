import os, json

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
        pass

    def update(self, metadata, media, lang):
        pass