   Json TV Show Metadata Agent for Plex
   ====================================
   Plex agent to load tv show metadata from JSON located in roto folder of library with yout tv show media.

   Media Structure
   ---------------
   This agent only supports TV Shows, agent for movies can be found [here](https://github.com/peter-kultan/JsonMovieAgent.bundle).

   TV Show Metadata should ve presented in `Info.json` file located at same directory as directory with TV Show name in first option and in same directory as media files in second option.

   There are two options to store TV Series, first one is:

   ```
   TV Shows
      |- Europe From Above
      |       |- S01
      |       |   |- E01.mkv
      |       |   |- 02.mp4
      |       |   \- E03.mpv
      |       \- 02
      |           |- 04.mkv
      |           \- E06.mp4
      |- Wednesday
      |   |- S01
      |       |- E04.mkv
      |       \- E05.mp4
      \- Info.Json
   ```
   This structure has direcotry with TV Shows names. This directory needs to be located at same directory as `Info.json` with metadata. Subdirs name covention needs to be S`seasonNumber` or only `seasonNumber` and in this directories should be episodes with name convension E`episodeNumber` or only `spisodeNumber`


   And second option is:
   ```
   TV Shows
      |- Wednesday s01E04.mp4
      |- Wednesday S01e05.mkv
      |- Europe From Above S04e01.mp4
      |- Europe From Above S04E02.mp4
      \- Info.json
   ```
   This structure directly contains video file in same directory with `Info.json`, and naming convention is `SeriesName` S`seasonNumber`E`episodeNumber`.

   And this two options can be combined (as showed bellow):
   ```
   TV Shows
      |- Europe From Above
      |       |- S01
      |       |   |- E01.mkv
      |       |   |- 02.mp4
      |       |   \- E03.mpv
      |       \- 02
      |           |- 04.mkv
      |           \- E06.mp4
      |- Wednesday s01E04.mp4
      |- Wednesday S01E05.mkv
      \- Info.json
   ```

   Example JSON
   ------------
   The `Info.json`file is structured to follow Plex TV Show Metadata Model as much as possible. It should look someting like (this example is for Wedensday season 1 episode 4).:

   ```json
   {
   "Wednesday":{
      "title":"Wednesday",
      "original_title":"Wednesday",
      "originally_available_at":"2022-11-23",
      "poster_path":"C:/shows/Wednesday.jpg",
      "genres":[
         "Sci-Fi & Fantasy",
         "Mystery",
         "Comedy"
      ],
      "countries":[
         "US"
      ],
      "studio":"",
      "summary":"Wednesday Addams is sent to Nevermore Academy, a bizarre boarding school where she attempts to master her psychic powers, stop a monstrous killing spree of the town citizens, and solve the supernatural mystery that affected her family 25 years ago — all while navigating her new relationships.",
      "rating":8.8,
      "seasons":{
         "01":{
            "originally_available_at":"2022-11-23",
            "title":"Season 1",
            "summary":"",
            "episodes":{
               "04":{
                  "title":"Woe What a Night",
                  "originally_available_at":"2022-11-23",
                  "summary":"Wednesday asks Xavier to the Rave'N dance, sparking Tyler's jealousy — but Thing's got something up his sleeve. Meanwhile, Eugene stakes out the cave.",
                  "rating":8.268
               }
            }
         }
      }
   }
}
   ```

   The keys if metadata are movie media file names with suffix. All fields in json file are optional. But first TV Show 'Wednesay' and its first season and its first episode has all metadata wich can be optained from json file.

   Instalation
   -----------
   1. Donwload the [zipped bundle](https://github.com/peter-kultan/JsonTVShowsAgent.bundle/archive/refs/heads/main.zip)
   2. Extract it
   3. ranem it to `JsonTVShowsAgent.bundle`
   4. Find the [Plex Media data directory](https://support.plex.tv/articles/202915258-where-is-the-plex-media-server-data-directory-located/)
   5. Move the .bundle folder to the Plug-ins directory.
   6. Restart plex server
   7. You should be able to see JsonTVShowsAgent in Agent settings and should be able to pick it in Libraries manager setting as TV Show library agent.