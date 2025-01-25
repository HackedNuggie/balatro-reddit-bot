import json
import praw
import re
import os

with open("data/blinds.json","r") as b, open("data/jokers.json","r") as j,open("data/abreviations.json","r") as a,open("data/vouchers.json","r") as v:
    blinds = json.load(b)
    jokers = json.load(j)
    abbrev = json.load(a)
    vouchers = json.load(v)

def matchSearch(group):
    group = group.lower()

    for blind in blinds:
            if blind["name"].lower() == group.lower():
                 return f"""
[**{blind["name"]}**](https://balatrogame.fandom.com/wiki/Blinds_and_Antes) Blind

- **Effect**: {blind["effect"]}
- **Beating the Blind**: Score at least {blind["multiplier"]} To earn {blind["earnings"]}

Data painstakingly pulled from [the fandom wiki](https://balatrogame.fandom.com/wiki/Balatro_Wiki).
"""
    for joker in jokers:
         if joker["name"].lower() == group:
              return f"""
[**{joker["name"]}**](https://balatrogame.fandom.com/{joker["name"].replace(" ","_")})

- **Effect**: {joker["effect"]}
- **Cost**: {joker["cost"]}
- **Rarity**: {joker["rarity"]}
- **Unlocking**: {joker["availability"]}

*Data painstakingly pulled from [the fandom wiki](https://balatrogame.fandom.com/wiki/Balatro_Wiki).*
"""
    for voucher in vouchers:
         if voucher["name"].lower() == group:
                upgraded, note = "",""
                if voucher["upgraded"] !="":
                    upgraded = f"- **Upgraded voucher**: {voucher['upgraded']}"
                if voucher["Note"] !="N/A":
                    if upgraded != "":
                         note += "\n"
                    note += f"- **Note**: {voucher['Note']}"
                return f"""
[**{voucher["name"]}**](https://balatrogame.fandom.com/Vouchers)

- **Effect**: {voucher["effect"]}
- **Unlocking**: {voucher["availability"]}
{upgraded}{note}

*Data painstakingly pulled from [the fandom wiki](https://balatrogame.fandom.com/wiki/Balatro_Wiki).*
"""
    return ""

if __name__  == "__main__":
    username = "other_balatro_bot"
    password = os.getenv("PASSWORD")
    client_id = os.getenv("CLIENT_ID")
    client_secret=os.getenv("CLIENT_SECRET")

    reddi_inst = praw.Reddit(
        client_id = client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent="test_bot"
    )

    subreddit = reddi_inst.subreddit("balatro")
    print(subreddit)

    print(matchSearch("Seed money"))
    submission = reddi_inst.subreddit("testingground4bots").stream.comments()
    print(submission)

    pattern = r"\[\[(.*?)\]\]"
    for x in submission:
        match = re.search(pattern,x.body)
        print(x.body)
        if match:
            if matchSearch(match.group(1)) != "":

                print(match.group(1))

