import json, requests, random, time, asyncio

valid = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def getUUIDFromMinecraft(minecraft):
    return json.loads(str(requests.get(f"https://api.mojang.com/users/profiles/minecraft/{minecraft}").content)[2:-1])["id"]

def createCode(minecraft, discord):
    minecraft = getUUIDFromMinecraft(minecraft)

    codes = json.loads(open("data/codes.json", "r").read())

    newCode = None

    while True:
        isCodeValid = True

        newCode = ""

        for i in range(2):
            newCode += valid[random.randint(0, len(valid) - 1)]

        for code in codes:
            if newCode == code:
                isCodeValid = False

        if isCodeValid: break

    codes[newCode] = {"minecraft": minecraft, "discord": discord, "expires": int(time.time()) + 500}
    
    open("data/codes.json", "w").write(json.dumps(codes))

    return newCode

def verifyCode(code, discord):
    codes = json.loads(open("data/codes.json", "r").read())

    try:
        codeData = codes[code]
    except:
        return False
    
    if not discord == codeData["discord"]: return False

    accounts = json.loads(open("data/accounts.json", "r").read())

    accounts[codeData["minecraft"]] = str(discord)

    open("data/accounts.json", "w").write(json.dumps(accounts))

    del codes[code]

    open("data/codes.json", "w").write(json.dumps(codes))

async def handleExpiredCodes():
    while True:
        codes = json.loads(open("data/codes.json", "r").read())

        codesNew = {}

        for code in codes:
            if not codes[code]["expires"] <= int(time.time()):
                codesNew[code] = codes[code]

        open("data/codes.json", "w").write(json.dumps(codesNew))

        await asyncio.sleep(1)