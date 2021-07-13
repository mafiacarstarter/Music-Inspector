# Music-Inspector

This is just a pair of python apps that I use to make playlists for me.
The Musical Cabinetmaker has you select all of the folders in which you have music.  It then proceeds to inspect every mp4 in those folders and makes a note of their duration.
Obviously this is a somewhat time consuming task, especially if you have a large number of files to process.
After it has finished, it saves that information in a Python cabinet file.

The GUI Playlist Maker opens the cabinet file made by the Musical Cabinetmaker.
It uses the information gathered earlier, along with your input, to make playlists.
You can choose which music folders should be enabled for the current playlist.
You can set the relative weight given to each of the folders when randomly selecting files.
You can set it to remove files from its list after they have been included in a playlist, and this option can be turned on or off for each folder separately.
You can, and probably should, set the length of your desired playlist in hours.
It provides a default name for the playlist it will make, but you can change that to whatever you would like.
After you have made a playlist, the default name will change to something else, allowing you to just spam playlists if you want.

The option at the top marked 'Bedtime' will add the contents of a playlist called './../end of night.m3u' to the end of the playlist it generates.
I used this to signal the end of the playlist, and give me warning time to wrap things up.

The Save and Load Weights buttons will save the weights as they are currently set, so that you can use the same weights some other time rather than having to remember them or recalculate them.
The Save Song Lists button will save the songlists back to the cabinet file from which it got them.  This is really only useful if you have it set to remove played songs from the playlist for some folder.

Enjoy!
