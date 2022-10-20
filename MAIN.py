# Before running, add the Bot token from the Discord Developer Portal
# and the general channel id in the on_ready function

import random
import discord
import numpy as np

# Replace with Discord Bot token
TOKEN = "*******************************************************"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

players = []
player_emoji = []

cards = ['3S', '3C', '3D',
         '3H', '4S', '4C', '4D', '4H', '5S', '5C', '5D', '5H', '6S', '6C', '6D', '6H', '7S', '7C',
         '7D', '7H', '8S', '8C', '8D', '8H', '9S', '9C', '9D', '9H', '10S', '10C', '10D', '10H', 'JS', 'JC', 'JD', 'JH',
         'QS', 'QC', 'QD', 'QH', 'KS', 'KC', 'KD', 'KH', '1S', '1C', '1D', '1H', '2S', '2C', '2D', '2H']

default_emoji = [':red_circle:', ':orange_circle:', ':yellow_circle:', ':green_circle:', ':blue_circle:',
                 ':purple_circle:', ':white_circle:', ':black_circle:', ':brown_circle:']

random.shuffle(default_emoji)
game_started = False
channel = None


def assign_cards(list_of_players):
    deck = np.arange(1, len(cards) + 1, 1)
    random.shuffle(deck)
    cards_dict = {}
    hand_length = len(deck) // len(list_of_players)

    start = 0
    end = hand_length

    for player in list_of_players:
        player_hand = deck[start:end].copy()
        player_hand.sort()
        cards_dict[player] = player_hand
        start += hand_length
        end += hand_length

    return cards_dict


def card_indexer(num):
    return -(num // -4)


def all_in_hand(playing, hand):
    return all([i in hand for i in playing])


def number_to_card(numbers):
    global cards
    return [cards[number - 1] for number in numbers]


def card_to_number(hand):
    global cards
    return [cards.index(card.upper()) + 1 for card in hand]


def assign_emoji(message, num_players):
    global default_emoji

    after_join = message.strip('join')
    if after_join != "" and after_join.startswith("!") and len(after_join) == 2:
        return after_join[1]
    else:
        return default_emoji[num_players % 9]


def is_four_of_a_kind(last_card, unique_values_in_hand, count_in_hand):
    last_card_is_single = len(last_card) == 1
    only_one_type = len(unique_values_in_hand) == 1
    four_cards = sum(count_in_hand) == 4
    return last_card_is_single and only_one_type and four_cards


def is_double_sequence(last_card, unique_values_in_hand, count_in_hand):
    no_twos = not any(unique_values_in_hand > 47)
    right_amount_of_cards = len(unique_values_in_hand) >= len(last_card) + 2
    only_doubles = sum(count_in_hand) == 2 * len(unique_values_in_hand)
    if len(unique_values_in_hand) > 1:
        max_one_diff = np.max(np.diff(unique_values_in_hand)) < 2
    else:
        max_one_diff = True

    return right_amount_of_cards and only_doubles and max_one_diff and no_twos


def follows_pattern(card_values, last_card, array_of_input):
    all_values_unique = len(np.unique(array_of_input)) == len(array_of_input)
    all_diff_same = sum(np.diff(card_values)) == sum(np.diff(card_indexer(last_card)))
    return all_values_unique and all_diff_same


def is_valid(unique_values_in_hand, count_in_hand, array_of_input):
    same_amount_of_all_values = len(unique_values_in_hand) * count_in_hand[0] == len(array_of_input)
    same_num_of_counts = len(np.unique(count_in_hand)) == 1
    if len(unique_values_in_hand) > 1:
        max_one_diff = np.max(np.diff(unique_values_in_hand)) < 2
    else:
        max_one_diff = True

    unique_cards_not_2 = len(count_in_hand) != 2
    return same_amount_of_all_values and same_num_of_counts and max_one_diff and unique_cards_not_2


def is_higher_than_last_card(list_of_input, last_card):
    return list_of_input[-1] > last_card[-1] and len(list_of_input) == len(last_card)


def delete_cards(array_of_input, hand):
    for card in array_of_input:
        hand = np.delete(hand, np.where(hand == card))
    return hand

# Replace channel id
@client.event
async def on_ready():
    global channel
    # Replace channel id
    channel = client.get_channel(00000000000000)

    print(f'We have logged in as {client.user}')
    await channel.send("Hello, I am a Bot which plays the card game Thirteen: \n"
                       "Type Join to join a game, then type Start when everyone is ready.\n"
                       "Go into your DMs to play the game.\n")


@client.event
async def display_hand(current_player, hand):
    await current_player.dm_channel.send(f"""```elm\n{str(hand).replace("'", "")}```""")


@client.event
async def congratulate(winner, winner_emoji, game_won):
    global players
    if game_won:
        icon = ":trophy:"
        winning_str = "game!"
    else:
        icon = ":medal:"
        winning_str = "round!"

    await dm_everyone(players, f"{winner_emoji} ***Yay! {winner} won the {winning_str}*** {winner_emoji}",
                      except_one_person=winner)
    await winner.dm_channel.send(
        f"{winner_emoji} ***{icon} Congratulations! You win the {winning_str} {icon}*** {winner_emoji}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_no_space = message.content.replace(" ", "").lower()

    if message_no_space == 'quit':
        await quit_player(message)

    if not game_started:

        if message_no_space.startswith('join'):
            await join_player(message)

        elif message_no_space == 'start' and len(players) > 0:
            await start_game(message)


@client.event
async def dm_everyone(people, message, except_one_person=None):
    for person in people:
        if person == except_one_person:
            continue
        else:
            await person.dm_channel.send(message)


@client.event
async def quit_player(message):
    global players
    global player_emoji
    global channel

    quitting_player = message.author

    if quitting_player in players:
        where_in_players = players.index(quitting_player)

        await channel.send(player_emoji[where_in_players] + f' {quitting_player} has quit the game')

        if str(message.channel) != 'general':
            await message.author.dm_channel.send('You have quit the game')

        players.remove(quitting_player)
        player_emoji.pop(where_in_players)


@client.event
async def join_player(message):
    global channel
    message_no_space = message.content.replace(" ", "").lower()
    joining_player = message.author

    if joining_player not in players:
        players.append(joining_player)
        emoji = assign_emoji(message_no_space, len(players))
        player_emoji.append(emoji)

        await channel.send(emoji + f' {joining_player} has joined the game')

        await message.author.create_dm()

        if str(message.channel) != 'general':
            await message.author.dm_channel.send('You have joined the game')


@client.event
async def start_game(message):
    global game_started
    global players
    global player_emoji
    global channel

    game_started = True
    after_start = True
    game_won = False

    await channel.send('Game Starting...')

    if str(message.channel) != 'general':
        await message.author.dm_channel.send('You have started the game')

    game_hands = assign_cards(players)

    for member in players:
        await member.dm_channel.send(f'Hi {member.name}')
        await display_hand(member, number_to_card(game_hands[member]))

    while not game_won:
        round_won = False
        turn = 0
        last_card = [0]
        first_go = True
        players_left = players.copy()
        display_turn = True

        while not round_won:

            if len(players) == 0:
                game_started = False
                return

            current_player = players[turn % len(players)]
            current_emoji = player_emoji[players.index(current_player)]

            if current_player not in players_left and len(players) > 1:
                turn += 1
                continue

            if display_turn:
                await dm_everyone(players, f"{current_emoji} **{current_player}'s Turn:**",
                                  except_one_person=current_player)
                display_turn = False

            hand = game_hands[current_player]

            if after_start:
                after_start = False
            else:
                await display_hand(current_player, number_to_card(hand))

            await current_player.dm_channel.send(f'{current_emoji} **Your Turn:**')

            def check(m):
                return m.author == current_player

            msg = await client.wait_for('message', check=check)
            msg_content = msg.content.replace(" ", "")

            if msg_content.lower() == "quit":
                turn += 1
                display_turn = True
                continue

            elif msg_content.lower() == "pass":

                if len(players) != 1:
                    players_left.remove(current_player)
                else:
                    await congratulate(current_player, current_emoji, round_won)
                    break

                await dm_everyone(players,
                                  f"{current_emoji} {current_player} has passed, they have {len(hand)} cards left",
                                  except_one_person=current_player)

                if len(players_left) == 1 and len(players) != 1:
                    round_winner = players_left[0]
                    round_winner_emoji = player_emoji[players.index(round_winner)]

                    await congratulate(round_winner, round_winner_emoji, game_won)

                    roll_by = len(players) - players.index(round_winner)
                    players = list(np.roll(players, roll_by))
                    player_emoji = list(np.roll(player_emoji, roll_by))

                    break

                else:
                    turn += 1
                    display_turn = True
                    continue

            else:
                try:
                    list_of_input = card_to_number(msg_content.split(','))
                except ValueError:
                    await current_player.dm_channel.send("Your input could not be understood, try again")
                    continue

                list_of_input.sort()

                if not all_in_hand(list_of_input, hand):
                    await current_player.dm_channel.send("You don't have all of these cards, try again")
                    continue

                array_of_input = np.array(list_of_input)
                card_values = card_indexer(array_of_input)

                unique_values_in_hand, count_in_hand = np.unique(card_values, return_counts=True)

                if is_higher_than_last_card(list_of_input, last_card) or first_go:
                    if first_go:
                        if not is_valid(unique_values_in_hand, count_in_hand, array_of_input):
                            await current_player.dm_channel.send(
                                "These cards do not form a sequence, try again")
                            continue

                        elif len(count_in_hand) > 1 and 13 in card_values:
                            await current_player.dm_channel.send(
                                "A 2 cannot form part of your sequence, try again")

                            continue
                        else:
                            last_card = array_of_input
                            first_go = False

                    if not follows_pattern(card_values, last_card, array_of_input):
                        await current_player.dm_channel.send(
                            "You cannot play these cards, they do not follow the same pattern, try again")
                        continue
                    else:
                        hand = delete_cards(array_of_input, hand)

                        await dm_everyone(players,
                                          f"{current_emoji} {current_player} has played {msg_content.upper()}, "
                                          f"they have {len(hand)} cards left",
                                          except_one_person=current_player)

                        if len(hand) > 0:
                            last_card = array_of_input

                        else:
                            game_won = True
                            await congratulate(current_player, current_emoji, game_won)
                            game_started = False
                            await dm_everyone(players, 'Type Start to play again, Type Quit to quit the lobby')
                            return

                elif last_card[-1] > 47 and (is_four_of_a_kind(last_card, unique_values_in_hand, count_in_hand) or
                                             is_double_sequence(last_card, unique_values_in_hand, count_in_hand)):

                    last_card = array_of_input

                    hand = delete_cards(array_of_input, hand)

                    await dm_everyone(players, f"{current_emoji} {current_player} has played "
                                               f"{msg_content.upper()}, they have {len(hand)} cards left",
                                      except_one_person=current_player)

                else:
                    await current_player.dm_channel.send(
                        "You cannot play these cards, they are not higher than the previous go, try again")
                    continue

                game_hands[current_player] = hand
                turn += 1
                display_turn = True


if __name__ == '__main__':
    client.run(TOKEN)
