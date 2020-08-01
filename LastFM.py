import sys

import spotipy
import spotipy.util as util
import pprint
import pylast
import json

username = 'jalexaacobs45'
playlist_id_spotify = 'spotify:playlist:1umFDa1LXFUTVDhPNa9pa3'



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

    #  playing around with searching for songs in spotify...
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, redirect_uri='https://example.com')

    if token:
        sp = spotipy.Spotify(auth=token)

        #TODO - add timestamp when updated to description - getting errors with this
        #(WIP) Grabs my weekly Top 20 songs from Last.fm and puts them in this playlist.
        # print(username)
        # print(playlist_id_spotify)
        # res = sp.user_playlist_change_details(username, playlist_id_spotify, description="testing lol")

        fail_count = 0 # count for every track that fails to be added 
        uri_list = []
        for i in range(len(topTracks)):
            try:
                q = topTracks[i]
                result = sp.search(q, limit=1,type="track")
                refined = result['tracks']['items'][0] # this fails sometimes - why?
                uri = (refined['uri'])
                uri_list.append(uri)
            except:
                # something went wrong, count it 
                fail_count += 1
            
        print(fail_count)
        sp.user_playlist_replace_tracks(username, playlist_id_spotify, uri_list) 


# from last fm
API_KEY = "30dd590f46f1e9d6e29d46765d85fa85"  # this is a sample key
API_SECRET = "7b168f6722c966e5174f7774aeef759f"

# authenticate
lfmUsername = "jalexaacobs"
password_hash = pylast.md5("Adamsandler62!")

# get network
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=lfmUsername, password_hash=password_hash)

jalex = network.get_authenticated_user()
#user2 = network.get_user("cthomas68")
#compareWeeklyTrackChartsImageDisplay(jalex,user2)

weeklyTrackWork(jalex)


