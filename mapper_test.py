#!/usr/bin/env python 

#with open('/home/kishna.bharat/full_devel.txt') as f:
import sys

unique_labels = ['Articles_containing_video_clips',
 'English-language_journals',
 'Windows_games',
 'American_film_directors',
 'American_people_of_Irish_descent',
 'Deaths_from_myocardial_infarction',
 'Guggenheim_Fellows',
 'Columbia_University_alumni',
 'Fellows_of_the_Royal_Society',
 'Major_League_Baseball_pitchers',
 'Harvard_University_alumni',
 'American_male_film_actors',
 'English-language_television_programming',
 'American_film_actresses',
 'American_male_television_actors',
 'American_films',
 'English-language_films',
 'Black-and-white_films',
 'American_drama_films',
 'Yale_University_alumni',
 'English-language_albums',
 'American_television_actresses',
 'American_comedy_films',
 'The_Football_League_players',
 'English_footballers',
 'British_films',
 'American_military_personnel_of_World_War_II',
 'Association_football_goalkeepers',
 'Serie_A_players',
 'Italian_footballers',
 'Association_football_midfielders',
 'Association_football_forwards',
 'English_cricketers',
 'Scottish_footballers',
 'French_films',
 'Insects_of_Europe',
 'Italian_films',
 'German_footballers',
 'Indian_films',
 'Main_Belt_asteroids',
 'Asteroids_named_for_people',
 'Rivers_of_Romania',
 'Russian_footballers',
 'Villages_in_the_Czech_Republic',
 'Association_football_defenders',
 'Australian_rules_footballers_from_Victoria_(Australia)',
 'Hindi-language_films',
 'Brazilian_footballers',
 'Villages_in_Turkey',
 'Arctiidae']


for line in sys.stdin:
    line = line.strip()
    line_list = line.split()
    line_no = line_list[0]
    labels = line_list[1].split(',')
    labels_decoded = [unique_labels.index(label) for label in labels]
    words = line_list[2:]
    #keys = line.split()
    for word in words:
        key = word
        value = 'd_ctr_' + line_no + '_' + str(labels_decoded)
	print ('{0}\t{1}'.format(key, value))
