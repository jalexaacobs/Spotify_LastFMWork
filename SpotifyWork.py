# # Shows the top artists for a user

# import sys
# import os
# import spotipy
# import spotipy.util as util


# # set SPOTIPY_CLIENT_ID='08b5db5ad1ef4643869316cc3aad0f69'
# # set SPOTIPY_CLIENT_SECRET='2ae992bb69b84d298c2e3a563c72d144'
# #export "SPOTIPY_REDIRECT_URI" = "http://localhost:8080"



# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()

# scope = 'user-top-read'
# token = util.prompt_for_user_token(username, scope, redirect_uri='https://example.com')

# print("lol")

# if token:
#     sp = spotipy.Spotify(auth=token)
#     print("wtf")
#     sp.trace = False
#     ranges = ['short_term', 'medium_term', 'long_term']
#     for range in ranges:
#         print("range:", range)
#         results = sp.current_user_top_artists(time_range=range, limit=50)
#         for i, item in enumerate(results['items']):
#             print(i, item['name'])
#         print()
# else:
#     print("Can't get token for", username)




import sys

import spotipy
import spotipy.util as util

username = 'jalexaacobs45'
playlist_id = 'spotify:playlist:1umFDa1LXFUTVDhPNa9pa3'
track_ids = ['spotify:track:4m32ZYmSYgGziMwx3cJxS7']


# if len(sys.argv) > 3:
#     username = sys.argv[1]
#     playlist_id = sys.argv[2]
#     track_ids = sys.argv[3:]
# else:
#     print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
#     sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, redirect_uri='https://example.com')

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    #results = sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_ids)
    results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    print(results)
else:
    print("Can't get token for", username)