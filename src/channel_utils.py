
def convert_to_int(channelId):
    try:
        if type(channelId) == int:
            return channelId
        elif type(channelId) == str:
            return int(channelId[2:len(channelId)-1])
    except Exception as e:
        print(e)
        return None