import sys

import spotipy
import spotipy.util as util
import pprint
import pylast
import json

username = 'jalexaacobs45'
playlist_id = 'spotify:playlist:1umFDa1LXFUTVDhPNa9pa3'



'''
Application name	Chrome New Tab Display
API key	30dd590f46f1e9d6e29d46765d85fa85
Shared secret	7b168f6722c966e5174f7774aeef759f
Registered to	jalexaacobs
'''

#prints the common top50 artists between two users
def compareTopArtists(user1,user2,artistLimit=50):
    #get topArtists for both users
    topArtists = user1.get_top_artists(limit=artistLimit)
    topArtists2 = user2.get_top_artists(limit=artistLimit)
    
    #convert to sets
    artistList1 = {str(artist[0]) for artist in topArtists}
    artistList2 = {str(artist[0]) for artist in topArtists2}
    
    #print common artists in top50
    comArtists = list(artistList2 & artistList1)   
    print("Common Top",artistLimit,"artists between",user1.get_name(),"and",user2.get_name(),":")
    for artist in comArtists:
        print(artist)

#prints the common tracks in the last week between two users 
def compareWeeklyTrackCharts(user1,user2):
    #get weekly charts
    chart1 = user1.get_weekly_track_charts()
    chart2 = user2.get_weekly_track_charts()
    
    #convert to sets and print common tracks
    set1 = {str(track[0]) for track in chart1}
    set2 = {str(track[0]) for track in chart2}
    comTracks = list(set1 & set2)
    print("Common tracks in the last week between",user1.get_name(),"and",user2.get_name(),":")
    for track in comTracks:
        print(track)


def compareWeeklyTrackChartsImageDisplay(user1,user2):
    #get weekly charts
    chart1 = user1.get_weekly_track_charts()
    chart2 = user2.get_weekly_track_charts()
    
    #convert to sets and print common tracks
    set1 = {track[0] for track in chart1}
    set2 = {track[0] for track in chart2}
    comTracks = list(set1 & set2)
    print("Common tracks in the last week between",user1.get_name(),"and",user2.get_name(),":")
    fout = open("output.html","w")
    for track in comTracks:
        print(str(track))
        try:
            writeToFile = "<img src=\"" + str(track.get_cover_image()) + "\"/>\n"
            fout.write(writeToFile)
        except:
            pass

    fout.close()
    


def weeklyTrackWork(user):
    '''
    PERIOD_OVERALL = "overall"
    PERIOD_7DAYS = "7day"
    PERIOD_1MONTH = "1month"
    PERIOD_3MONTHS = "3month"
    PERIOD_6MONTHS = "6month"
    PERIOD_12MONTHS = "12month"
    '''
    # get top tracks for the lasts week
    topTracks = jalex.get_top_tracks(period='7day', limit=20)
    topTracks = [str(topTracks[i][0]) for i in range(len(topTracks))]
    # for i in range(len(topTracks)):
    #     print(topTracks[i])

    #  playing around with searching for songs in spotify...
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, redirect_uri='https://example.com')

    if token:
        sp = spotipy.Spotify(auth=token)
        
        #TODO - make it r+ and then keep the file open for the read and write

        # load in old ids to remove 
        try: # needs to be a try in case the data file doesnt exist
            with open('data.json', 'r', encoding='utf-8') as infile: 
                old_ids = json.load(infile)
                print("old ids coming up: ", old_ids)

            # print(old_ids)
            for i in range(len(old_ids)):
                print(old_ids[i])
                results = sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, old_ids[i])
        except FileNotFoundError:
            # this means the file doesnt exist and, it will be created later so do nothing
            pass

        # THANKS GITHUB https://github.com/plamere/spotipy/issues/33
        #q = "artist:Rolling Blackout AND track:French"
        uri_list = []
        for i in range(len(topTracks)):
            q = topTracks[i]
            result = sp.search(q, limit=1,type="track")
            #pprint.pprint(result)
            refined = result['tracks']['items'][0]
            uri = [(refined['uri'])]
            pprint.pprint(uri)

            
            # uncomment to remove from PL

            
            #results = sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, uri)


            # add to playlist
            results = sp.user_playlist_add_tracks(username, playlist_id, uri)

            #TODO - Add a date when last updated

            print(results)

            uri_list.append(uri)


        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(uri_list, f, ensure_ascii=False, indent=4)    
        #print(json.dumps(uri_list))


    # if token:
    #     sp = spotipy.Spotify(auth=token)
    #     sp.trace = False
    #     #results = sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_ids)
    #     results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    #     print(results)
    # else:
    #     print("Can't get token for", username)

    # for track in topTracks:
    #     print(str(track[0]))


# from last fm
API_KEY = "30dd590f46f1e9d6e29d46765d85fa85"  # this is a sample key
API_SECRET = "7b168f6722c966e5174f7774aeef759f"

# authenticate
username = "jalexaacobs"
password_hash = pylast.md5("Adamsandler62!")

# get network
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)

jalex = network.get_authenticated_user()
#user2 = network.get_user("cthomas68")
#compareWeeklyTrackChartsImageDisplay(jalex,user2)

weeklyTrackWork(jalex)


