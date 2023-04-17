import json
# https://github.com/T-vK/chord-collection

# read chords.json file
chords_file = json.loads(open('chord-fingerings.json', 'r').read())
response = json.loads(open('response.json', 'r').read())

prog = ['F', 'Fmaj', 'Fmin', 'Fm', 'Fdim', 'Faug', 'F7', 'Fmaj7', 'Fmin7', 'Fm7', 'Fdim7', 'Fadd9', 'Fm7b5', 'Fø7', 'Fø']

chords = list(chords_file.keys())

chord_list = []
for alternates in response['alternates']:
    chord_list.extend(alternates['reharmonized'])
    chord_list.extend(alternates['new_passing_chords'])

chord_list = list(set(chord_list))
# print(len(chord_list), len(set(chord_list)))

chord_fingerings = dict()
for chord in chord_list:
    for key in chords_file.keys():
        
        if chord == key:
            # print(key, chord)
            for position in chords_file[key]:
                if chord not in chord_fingerings:
                    chord_fingerings[chord] = []
                chord_fingerings[chord].append(position)
            break

for k,v in chord_fingerings.items():
    # print(k, len(v))
    chord_fingerings[k] = v[0:3]

for k,v in chord_fingerings.items():
    print(k, v)

response['chord_fingerings'] = chord_fingerings


'''
for pchord in prog:
    current_chord = ''
    if pchord[-3:len(pchord)] == 'maj':
        # print('found major')
        current_chord = pchord[0] if pchord[1] != '#' and pchord[1] != 'b' else pchord[0:2]
    elif pchord[-3:len(pchord)] == 'min':
        # print('found minor')
        current_chord = pchord[0] if pchord[1] != '#' and pchord[1] != 'b' else pchord[0:2] + 'm'
    elif pchord[-4:len(pchord)] == 'min7':
        # print('found minor 7')
        current_chord = pchord[0] if pchord[1] != '#' and pchord[1] != 'b' else pchord[0:2] + 'm7'
    elif 'ø' in pchord:
        if '#' in pchord or 'b' in pchord:
            current_chord = pchord[0:2] + 'm7b5'
        else:
            current_chord = pchord[0] + 'm7b5'
        

    else:
        current_chord = pchord

    
    if current_chord not in chords:
        print('NOT FOUND: ', pchord)
        break
    else:
        print(current_chord)
        for chord in chords_file[current_chord]:
            print(chord['positions'])
    print('----')
# for pchord in prog:
    # chords = list(filter(lambda chord: chord['key'] == pchord, chords_file))
'''

# for pchord in prog:
#     found = False
#     for chord in chords:
#         if pchord == chord['key']+chord['suffix']:
#             # print('FOUND: ', pchord)
#             found = True
#             continue
#     if not found:
#         print('NOT FOUND: ', pchord)

# print(len(chords))

# minor -> m
# minor 7 -> m7
# major 7 -> maj7
# dominant 7 -> 7
# half-diminished 7 -> dim7


# for chord in chords:
#     if 'C#major' == chord['key']+chord['suffix']:
#         print(chord['frets'])