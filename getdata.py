import cassiopeia as cass
import random
import arrow
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch, Match, Season
from cassiopeia.data import Role, Lane, Division, Tier
from getmmr import get_mmr
import json

conf = json.loads(open("config.json", "r").read())
cass.set_riot_api_key(conf["API_Key"])
cass.set_default_region("NA")


full_matches = []
position_int = {"TOP": 0, "JG": 1, "MID": 2, "ADC": 3, "SUPP": 4}

div_int = {Division.one: 3, Division.two: 2, Division.three: 1, Division.four: 0}
tier_int = {Tier.iron: 0, Tier.bronze: 1, Tier.silver: 2, Tier.gold: 3, Tier.platinum: 4, Tier.diamond: 5, Tier.master: 6, Tier.grandmaster: 7, Tier.challenger: 8}


def get_position(role: str, lane: str):
    if(role == Role.duo_carry):
        return "ADC"
    elif(role == Role.duo_support):
        return "SUPP"
    if(lane == Lane.jungle):
        return "JG"
    if(lane == Lane.top_lane):
        return "TOP"
    if(lane == Lane.mid_lane):
        return "MID"

def get_rank_score(tier, div):
    return tier_int[tier]*4 + div_int[div]


def get_accounts_in_league(summoner_name: str, region: str):
    acc_ids = []
    summoner = Summoner(name=summoner_name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)

    entries = summoner.league_entries
    print(f"Listing all summoners in this league:")
    for entry in entries.fives.league.entries:
        acc_ids.append(entry.summoner)
    return acc_ids

def get_matches(summoner):
    patch = Patch.from_str("10.8", region="NA")
    print(patch.start)
    end_time = patch.end
    if end_time is None:
        end_time = arrow.now()

    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_9}, queues={Queue.ranked_solo_fives}, begin_time=1585206000)
    return match_history



search_accounts = ["jonathanh1386", "Exdiark", "eMuffin", "JLHERPES", "brobro420", "X9Squared", "dna replication", "dwen"]
for username in search_accounts:
    league_acc = get_accounts_in_league(username, "NA")
    random.shuffle(league_acc)
    for acc in league_acc[:5]:
        full_matches.extend(get_matches(acc))


for m in full_matches:
    name_pos = []
    w = True
    for p in m.blue_team.participants:
        if(Queue.ranked_solo_fives not in p.summoner.ranks):
            w = False
            break
        rkdat = p.summoner.ranks[Queue.ranked_solo_fives]
        name_pos.append((p.summoner.name, get_position(p.role, p.lane), get_rank_score(rkdat.tier, rkdat.division)))

    if(w == False):
        continue

    w = True
    for p in m.red_team.participants:
        if(Queue.ranked_solo_fives not in p.summoner.ranks):
            w = False
            break
        rkdat = p.summoner.ranks[Queue.ranked_solo_fives]
        name_pos.append((p.summoner.name, get_position(p.role, p.lane), get_rank_score(rkdat.tier, rkdat.division)))

    if(w == False):
        continue

    print(name_pos)

    seen = [0 for _ in range(5)]
    for name, pos, rank in name_pos[:5]:
        if(pos not in ["TOP", "JG", "MID", "ADC", "SUPP"]):
            print("ERROR: Missing positional info!")
            break
        seen[position_int[pos]] = 1
    if(0 in seen):
        print("ERROR: Missing positional info!")
        continue

    seen = [0 for _ in range(5)]
    for name, pos, rank in name_pos[5:10]:
        if(pos not in ["TOP", "JG", "MID", "ADC", "SUPP"]):
            print("ERROR: Missing positional info!")
            break
        seen[position_int[pos]] = 1
    if(0 in seen):
        print("ERROR: Missing positional info!")
        continue

    final_out = []

    w = True
    for name, pos, rank in name_pos:
        final_out.append((pos,rank))

    if(w == True):
        print("FULLY PROCESSED MATCH\t" + str(m.id))
        open("output.txt", "a+").write("\n".join(list(map(str, final_out))) + "\n" + str(m.blue_team.win) + "\n")




