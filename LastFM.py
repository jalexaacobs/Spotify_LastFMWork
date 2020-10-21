import sys
import datetime
import spotipy
import spotipy.util as util
import pprint
import pylast
import json

username = 'jalexaacobs45'
alex_playlist = '1umFDa1LXFUTVDhPNa9pa3'
grace_playlist = '6d994pPxkHN2gnUSfZzAWH'


# commented code below is from alex playing around with other things


# #prints the common top50 artists between two users
# def compareTopArtists(user1,user2,artistLimit=50):
#     #get topArtists for both users
#     topArtists = user1.get_top_artists(limit=artistLimit)
#     topArtists2 = user2.get_top_artists(limit=artistLimit)
    
#     #convert to sets
#     artistList1 = {str(artist[0]) for artist in topArtists}
#     artistList2 = {str(artist[0]) for artist in topArtists2}
    
#     #print common artists in top50
#     comArtists = list(artistList2 & artistList1)   
#     print("Common Top",artistLimit,"artists between",user1.get_name(),"and",user2.get_name(),":")
#     for artist in comArtists:
#         print(artist)

# #prints the common tracks in the last week between two users 
# def compareWeeklyTrackCharts(user1,user2):
#     #get weekly charts
#     chart1 = user1.get_weekly_track_charts()
#     chart2 = user2.get_weekly_track_charts()
    
#     #convert to sets and print common tracks
#     set1 = {str(track[0]) for track in chart1}
#     set2 = {str(track[0]) for track in chart2}
#     comTracks = list(set1 & set2)
#     print("Common tracks in the last week between",user1.get_name(),"and",user2.get_name(),":")
#     for track in comTracks:
#         print(track)


# def compareWeeklyTrackChartsImageDisplay(user1,user2):
#     #get weekly charts
#     chart1 = user1.get_weekly_track_charts()
#     chart2 = user2.get_weekly_track_charts()
    
#     #convert to sets and print common tracks
#     set1 = {track[0] for track in chart1}
#     set2 = {track[0] for track in chart2}
#     comTracks = list(set1 & set2)
#     print("Common tracks in the last week between",user1.get_name(),"and",user2.get_name(),":")
#     fout = open("output.html","w")
#     for track in comTracks:
#         print(str(track))
#         try:
#             writeToFile = "<img src=\"" + str(track.get_cover_image()) + "\"/>\n"
#             fout.write(writeToFile)
#         except:
#             pass

#     fout.close()
    


def weeklyTrackWork(user, playlist_id_spotify):
    '''
    PERIOD_OVERALL = "overall"
    PERIOD_7DAYS = "7day"
    PERIOD_1MONTH = "1month"
    PERIOD_3MONTHS = "3month"
    PERIOD_6MONTHS = "6month"
    PERIOD_12MONTHS = "12month"
    '''
    # get top tracks for the lasts week - get 30 for some buffer for failure
    topTracks = user.get_top_tracks(period='7day', limit=30)
    topTracks = [str(topTracks[i][0]) for i in range(len(topTracks))]

    #  playing around with searching for songs in spotify...
    scope = 'playlist-modify-public'

    #TODO - fix this, do i even need a redirect_uri?
    token = util.prompt_for_user_token(username, scope, redirect_uri='https://example.com')

    if token:
        sp = spotipy.Spotify(auth=token)

        # update the description with current date and time that it was just updated last
        dateNow = datetime.datetime.now()
        dateString = dateNow.strftime("%x") + " at " + dateNow.strftime("%I") + ":" + dateNow.strftime("%M") + " " + dateNow.strftime("%p")
        descString = "Updates the top 20 from the last week according to LastFM. Last updated on " + dateString + "."
        sp.user_playlist_change_details(username, playlist_id_spotify, description=descString)
        
        #TODO - try/except if connected to internet

        fail_count = 0 # count for every track that fails to be added 
        uri_list = []
        for i in range(len(topTracks)):
            if i < 20 + fail_count: #loop until 20 tracks can be added
                try:
                    q = topTracks[i]
                    result = sp.search(q, limit=1,type="track")
                    refined = result['tracks']['items'][0] # this fails sometimes - why?
                    uri = (refined['uri'])
                    uri_list.append(uri)
                except:
                    # something went wrong, count it 
                    fail_count += 1

        sp.user_playlist_replace_tracks(username, playlist_id_spotify, uri_list) 

# load credentials from local file 
# put LastFM information (e.g. key, secret, password) in this json file
with open('.credentials.json','r') as f:
  credentials = json.load(f)

# from last fm
API_KEY = credentials["LastFM_API_Key"] 
API_SECRET = credentials["LastFM_API_Secret"]

# authenticate
lfmUsername = "jalexaacobs"
password_hash = pylast.md5(credentials["LastFM_Password"])

# get network
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=lfmUsername, password_hash=password_hash)

# get last fm user running the show 
jalex = network.get_authenticated_user()

# get the top 20s for both alex and grace
weeklyTrackWork(jalex, alex_playlist)
weeklyTrackWork(network.get_user("gracemjacobs"),grace_playlist)
