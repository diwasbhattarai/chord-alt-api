import re

progression = '[C#maj, C#min, C#dim, C#aug, C#7, C#maj7, C#min7, C#dim7, C#add9]'
progression = progression[1:-1]
progression = progression.split(', ')

for chord in progression:
    # use regex to check if the chord is in the correct format
    # chord format includes maj, min, dim, aug, dominant 7, major 7, minor 7, half-diminished 7, diminished 7, and add9
    # the expression should not match malicious string like 'C#may not be a chord'
    
    if re.match(r'^[A-G][#]?(maj|min|dim|aug|7|maj7|min7|dim7|add9)?$', chord) == None:
        print('Chord is invalid ', chord)
    else:
        print('Chord is valid ', chord)
    
