import requests
import json
import sqlite3
import APIKeys
import spotipy
import spotipy.oauth2 as oauth2
import MusicGrab
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
py.sign_in("erbrynn", "5EFtk0fjjKieVEDBDApc")

conn = sqlite3.connect("spotify.sqlite")
cur = conn.cursor()

f = open("rawmusicdata.json", "w")

# get top spotify data and put into dictionary
music_data = {}
cur.execute("SELECT song_title, rating FROM SpotifySongData")
for row in cur:
    song = row[0]
    rating = row[1]
    if song not in music_data:
        music_data[song] = rating
    else:
        music_data[song] += rating

cur.execute("SELECT song_title, rating FROM TopSpotifyData")
for row in cur:
    song = row[0]
    rating = row[1]
    if song not in music_data:
        music_data[song] = rating
    else:
        music_data[song] += rating

cur.execute("SELECT song, rating_billboard FROM BillboardData")
for row in cur:
    song = row[0]
    rating = row[1]
    if song not in music_data:
        music_data[song] = rating
    else:
        music_data[song] += rating

music_string = json.dumps(music_data)
f.write(music_string)
f.close()

sorted_music = sorted(music_data.items(), key = lambda x : x[1])
tup_lst= sorted_music[:25]


labels = []
values = []
for song in tup_lst:
    labels.append(song[0])
    values.append(song[1])

data = [
    go.Bar(
        x=labels,
        y=values,
        marker = dict(
            color = "rgb(110, 193, 136)"
        )
    )
]

layout = go.Layout(
    title="Song Ratings",
    autosize=False,
    width = 1100,
    height = 1000,
    yaxis=go.layout.YAxis(
        title="Ratings",
        ticktext = values,
        automargin=True,
        titlefont=dict(size=30),
    ),
    xaxis=go.layout.XAxis(
        ticktext = labels,
        automargin=True,
        titlefont = dict(size=30),
    )

)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='automargin')
plot_url = py.plot(fig)

'''Start new visualization


'''
title = "Top Ten Song Ratings Over Time"
cur.execute("SELECT song_title, rating FROM TopSpotifyData")
top_wed_dictionary = {}
for row in cur:
    song = row[0]
    rating = row[1]
    if song not in top_wed_dictionary:
        top_wed_dictionary[song] = rating
    else:
        top_wed_dictionary[song] += rating

sorted_top_music = sorted(top_wed_dictionary.items(), key = lambda x : x[1])
top_tup_lst= sorted_top_music[:10]

top_labels = []
top_ratings = []
for song in top_tup_lst:
    top_labels.append(song[0])
    top_ratings.append(song[1])

cur.execute("SELECT song_title, rating FROM SpotifySongData")
top_sat_dictionary = {}
for row in cur:
    song = row[0]
    rating = row[1]
    if song not in top_sat_dictionary:
        top_sat_dictionary[song] = rating
    else:
        top_sat_dictionary[song] += rating

overall_dict = {}
for song in top_labels:
    overall_dict[song] = [top_wed_dictionary[song], top_sat_dictionary[song]]

x_data = [
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"],
    ["4/17", "4/20"]
]
y_data = list(overall_dict.values())

labels = list(overall_dict.keys())
colors = ["#011936", "#465362", "#82A3A1", "#9FC490", "#C0DFA1", "#B2C2DF", "#A1483B",
"#E4B5E0", "#72AEC3", "#DA99A8"]

traces = []

for i in range(10):
    traces.append(go.Scatter(
        x=x_data[i],
        y=y_data[i],
        mode = "lines",
        line = dict(color = colors[i], width=5),
        connectgaps = True,
    ))
    traces.append(go.Scatter(
        x = [x_data[i][0], x_data[i][1]],
        y = [y_data[i][0], y_data[i][1]],
        mode = "markers",
        marker = dict(color = colors[i])
    ))

layout = go.Layout(
    xaxis = dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor="rgb(204, 204, 204)",
        linewidth=5,
        ticks="outside",
        tickcolor="rgb(204,204,204)",
        tickwidth=2,
        ticklen=5,
        tickfont=dict(
            family="Arial",
            size=20,
            color="rgb(0,0,0)",
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=300,
        r=20,
        t=110,
    ),
    showlegend=False
)

annotations = []
# labeling different lines and graphs
for y_trace, label, color in zip(y_data, labels, colors):
    annotations.append(dict(xref="paper", x=0.05, y=y_trace[0],
    xanchor="right", yanchor="middle", text="{} {}".format(label, y_trace[0]), 
    font=dict(family="Arial", size=12), showarrow=False))

    annotations.append(dict(xref='paper', x=0.95, y=y_trace[1], xanchor='left',
    yanchor='middle', text='{}'.format(y_trace[1]), font=dict(family='Arial', size=12),
    showarrow=False))

annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05, 
xanchor='left', yanchor='bottom', text='Top 10 Song Ratings Over Time', 
font=dict(family='Arial', size=30, color='rgb(0,0,0)'), showarrow=False))

layout["annotations"] = annotations

fig = go.Figure(data=traces, layout=layout)
py.iplot(fig, filename = "overtimelinegraph")
plot_url = py.plot(fig)



    

