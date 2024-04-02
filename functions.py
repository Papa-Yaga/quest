def search_object(current_room, object_relations, user_input, game_state):
    try:
      if object_relations[user_input][0]["type"] == "key":
        related_item = object_relations[user_input][0]["name"]
        print(f"Congratulations, you found {related_item}. Enter a door to try opening it.")
        game_state["keys_collected"].add(related_item)
      else:
        print(f"You find nothing in {user_input.title()}.")
    except KeyError:
      print("That does not exist.")
    except IndexError:
      print(f"You find nothing in {user_input.title()}.")
    # related_items = object_relations["couch"]

# search_object(game_room, object_relations)

def explore_room(current_room, object_relations):

    """
    This allows the player explore the current room and discover the items. Parameters: current_room (dict):
    The dictionary representing the current room to be explored.
    Returns: A list of strings representing the names of the items found in the current room.
    """


    room_items = [item["name"] for room, items_list in object_relations.items() if room == current_room for item in items_list]
    print("Items in the room:", room_items)
    return room_items

#  This is Sergejs Cell. -- Please Do not touch --

def enter_door(current_room, keys, game_state, object_relations, all_keys):
  """
  docstrings incoming...
  """

  user_input = input(f"Which door would you like to try to open?")
  try:
    if current_room in object_relations[user_input]:
      for k in all_keys:
        if k["target"] == user_input and k["name"] in game_state["keys_collected"]:
          next_room = [room["name"] for room in object_relations[user_input] if room != current_room][0]
          return next_room
    else:
      print(f"Please pick a door in {current_room['name']}")
      return current_room
  except IndexError:
    print("This door does not exist... try again.")

def examine_object(current_room, object):
  """
  This brings the player to examine a specific object in the current room,
  The function prints out information or a description of the examined object if it is found in the room.
  Parameters:current_room (dict): The dictionary representing the current room where the object is located.
  """

  print(f"You take a look at the {object}.")
  for thing in current_room:
    if thing["name"] == object:
      print(thing["desc"])

def check_inventory(state):
  for item in state:
    print(f"You have a {item}")

def start_game(current_room, game_state, object_relations, all_keys, all_rooms):
  """
  This function starts the game by setting the initial room where the player begins.
  Parameters: current_room (dict)represents the initial room where the player/user starts.
  """

  target_room = game_state["target_room"]

  print("You wake up in an escape room in indonesia.")
  while current_room != target_room:

    for room in all_rooms:
      if room["name"] == current_room:
        current_room = room

    user_input = input(f"\n You are in {current_room['name']}. What would you like to do now? You can explore the room, examine an object, search an object or check your inventory.")
    if "explore" in user_input:
      [*items] = explore_room(current_room["name"], object_relations)
    elif "examine" in user_input:
      try:
        for i in [*items]:
          if i in user_input.lower():
            examine_object(object_relations[current_room["name"]], i)
      except Exception as e:
        print("Try exploring the room first...")
    elif "search" in user_input:
      for i in object_relations[current_room["name"]]:
        if i["name"] in user_input:
          search_object(current_room, object_relations, i["name"], game_state)
          #if i["type"] == "door":
            #current_room = enter_door(current_room,i["name"],game_state["keys_collected"], object_relations)
    elif "check" in user_input:
      check_inventory(game_state["keys_collected"])
    elif "door" in user_input:
      # for x in object_relations[current_room["name"]]:
        # if x["type"] == "door":
          # door = x["name"]
      current_room = enter_door(current_room, game_state["keys_collected"], game_state, object_relations, all_keys)
    else:
        print("You have to choose something. Please type 'explore', 'examine', 'search', 'check' or 'door'.")

