# This script was written by Greg Guyles to plot 
# the timestamps of geocoded and not-geocoded
# tweets for each users of a provided list
# Required Python packages:
#     numpy
#     matplotlib

import re
import time
import json
import matplotlib.pyplot as plt
import numpy as np
import load_users
import sys

# Load Users of interest into an array
# this list is of the format:
#     username_<unique ID>
# Users will be plotted in the order of this array
interesting_users = load_users.order_pre()

# Load Users of interest into an array
# this list is of the format:
#     username
# These are the same usernames to be displayed along the 
# y-axis, these are the same users as the above list. At 
# the time this was quicker than a non-redundant solution
interesting_usernames = load_users.order_pre_name()

# Provide the output filename
filename = 'graph_01'

# Top level data directoryy
tweet_dir = "../../data/final/user_data"

# Start and End Date/Time in Unix time
start_day = 1372658400
end_day   = 1383112800

num_users = len(interesting_users)
re_letter = re.compile("[a-z | A-Z]")

# Create figure object
fig = plt.figure(figsize=( 12, num_users * 0.20))
ax = fig.add_axes([0.15, 0.02, 0.75, 0.95])
ax.set_ylim(-1, len(interesting_users) + 4)

# y-axis tick marks, one per username
yticks = np.arange(0, num_users, 1)
ax.set_yticks(yticks)
ax.set_yticklabels(interesting_usernames)

# limit the x-axis time period
ax.set_xlim(start_day, end_day)
xticks = []
xticks_lab = []

# Add 1 X-axis tick per day
while start_day <= end_day:
      day = 0
      xticks.append(start_day)
      start_day += 60 * 60 * 24
      xticks_lab.append(day)
      day += 1
ax.set_xticks(xticks)
ax.set_xticklabels([])

# set the output text filename, this was used to look up usernames
# by index before they were added to the y-axis of the graphic
user_list_file = open(filename + '_users.txt', 'w+')
user_list  = filename + "\n" + '#' * 32 + '\n'

# loop through the interesting_users array
for user_idx, user in enumerate(interesting_users):
      user_list += '%2i%30s\n' % (user_idx, user)
      oldest_time = 0
      file_dir = ""
      # determine sub-directory for this username
      if re_letter.match(user, 0):
            sub_dir = user[0].lower()
      else:
            sub_dir = "non"

      # find the directory and filename of this users data
      file_dir = tweet_dir + "/" + sub_dir + "/" + user.lower() + ".json"

      # open the file
      with open(file_dir) as f:
            pre_geo_ct = 0
            pet_not_geo_ct = 0
            geo_list = []
            non_geo_list = []
            for line in f:
                  jfile = json.loads(line)

                  # Get unix time stamp
                  timestamp = jfile['created_at']
                  time_tuple = time.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y")
                  unix_time = int(time.mktime(time_tuple))

                  # Get geo coded status
                  # if not a retweet
                  if not 'retweeted_status' in jfile:
                        # if the tweet has a "coordinates" entry append its timestamp
                        # to the geo_list
                        if jfile['coordinates']:
                              geo_list.append(unix_time)
                              if unix_time > oldest_time:
                                    oldest_time = unix_time
                        # otherwise append the timestamp to non_geo_list
                        else:
                              non_geo_list.append(unix_time)
                              if unix_time > oldest_time:
                                    oldest_time = unix_time

            # plot the geo_list and non_geo_list arrays in different colors
            ax.plot(non_geo_list, [user_idx] * len(non_geo_list), '|', color='#00324C')                   
            ax.plot(geo_list, [user_idx] * len(geo_list), '|', color='#ED5900')

# Annotation to highlight the period of heavy flood activity
ax.fill([1378706400, 1379916000, 1379916000, 1378706400], 
      [-1, -1, num_users, num_users], 
      color='#FFFDE2')

# Annotation to denote important dates
ax.annotate('9/09/13', xy=(1378706400, num_users), xytext=(1378706400 - (60*60*24*3.5), 
      num_users + 2), arrowprops=dict(arrowstyle="->"))
ax.annotate('9/23/13', xy=(1379916000, num_users), xytext=(1379916000 - (60*60*24*3.5), 
      num_users + 2), arrowprops=dict(arrowstyle="->"))
ax.annotate('7/01/13', xy=(1372658400 + (60*60*24*1), num_users+2))
ax.annotate('10/30/13', xy=(end_day - (60*60*24*8), num_users+2))

# withe users text file
user_list_file.write(user_list)
user_list_file.write('#' * 32 + '\n')
user_list_file.close()

# Save the image to a file
fig.savefig(filename + ".png", dpi=600)

# Uncommenting the below line will display the image 
# fig.show()