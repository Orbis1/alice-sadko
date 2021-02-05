quest_order = ['kupol', 'zvonnitsa', 'cathedral']

place_seen = 'kupol'

def next_place(place, quest_order=quest_order):
  current = quest_order.index(place)
  next = False if current == len(quest_order)-1 else quest_order[current+1]
  

myTuple = ("John", "Peter", "Vicky")

x = place_seen +'\n'+ 'ss'

print(x)