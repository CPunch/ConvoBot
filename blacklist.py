def passFilter(msg):
    # lets make sure it isn't an empty message or a shitpost
    return len(msg) > 0 and not 'http' in msg