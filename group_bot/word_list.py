# group_bot/word_list.py
# @roshhellwett makaut tele bot - Zenith Supreme Multi-lingual Database

BANNED_WORDS = [
    # --- [EN] Stage 1 & 2 English ---
    "ass", "asshole", "bastard", "bitch", "bloody", "bollocks", "bullshit",
    "cock", "cocksucker", "crap", "cunt", "dick", "dickhead", "fag", "faggot",
    "fuck", "fucked", "fucker", "fucking", "fuckoff", "jerk", "motherfucker",
    "moron", "piss", "pissed", "prick", "pussy", "shit", "shitty", "slut",
    "sonofabitch", "whore", "wanker", "wtf", "arse", "arsehole", "arsewipe", 
    "arseface", "bugger", "buggeroff", "knob", "knobhead", "bellend", "balls", 
    "ballsack", "ballbag", "scumbag", "scum", "shithead", "shitface", "shitbag", 
    "shitstain", "dipshit", "jackass", "jackhole", "jerkoff", "wankstain", "twat", 
    "twatface", "twathead", "douche", "doucebag", "slag", "skank", "hoe", "hoebag", 
    "tramp", "pisshead", "retard", "retarded", "numpty", "wazzock",

    # --- [HI] Stage 1 & 2 Hindi / Hinglish (Romanized) ---
    "chutiya", "chutia", "chutiye", "chut", "chutmarika", "gand", "gandu",
    "gaandfat", "gaandmasti", "haraami", "harami", "haramkhor", "bhosdiwale",
    "bhosdike", "bhosdiwala", "bhenchod", "behenchod", "bahenchod", "madarchod",
    "maadarchod", "maa-ki-chut", "maa-ki-aankh", "betichod", "bhaichod", 
    "lauda", "laode", "lund", "land", "randi", "raand", "randwa", "randibaz",
    "suar", "sooar", "kutte", "kutta", "kutti", "kuttiya", "ullu", "ulluka-patha",
    "chudai", "chudne", "chodna", "chodenge", "chodu", "chichora", "kamina", 
    "kamini", "kamine", "kaminey", "haramzadah", "haramzaadah", "haramzaadi", 
    "haramzadi", "haram ki aulaad", "harami ke bacche", "suar ki aulaad", 
    "kutte ki aulaad", "suar ka bachcha", "kutte ka bachcha", "bhand", "bhandwa", 
    "bhadwa", "bhadwaa", "rakhail", "hijrah", "hijdah", "hijda", "saala", "chhakkah", 
    "chakka", "meetha", "katua", "mulla", "mulle", "khotta", "tatte", "tatti", 
    "tattee", "tatty", "saala", "salasali", "sali", "nalayak", "nikamma", "nalayak kutta",

    # --- [HI] Stage 1 & 2 Devanagari ---
    "चुतिया", "চুতিয়া", "गांडू", "हरामी", "हरामखোর", "भोसड़ीके", "बहनचोদ",
    "মাদারচোদ", "রাंडी", "সুআর", "কুত্তা", "কুত্তী", "ঊল্লু", "চুদাই", "कमीना", 
    "कमीनी", "कमीने", "हरामज़ादा", "हरामज़ादी", "हराम की औलाद", "हरामी के बच्चे", 
    "सुअर की औলাদ", "कुत्ते की औलाद", "भंड", "भड़वा", "रখৈল", "হিজড়ো", "ছক্কো", 
    "মীঠো", "কটুআ", "মুল্লা", "তট্টি", "সালা", "সালী", "নালায়ক",

    # --- [BN] Stage 1 & 2 Bengali (Bangla Script) ---
    "চোদা", "চোদাচুদি", "চোদচুদি", "চোদান", "চোদানোর", "চুদাচুদি", "চুদানি",
    "চুদি", "চুদিরবাজ", "চুতমারানি", "চুতিয়া", "চুতমারানিরবাচ্চা", "চুতমারানিরপোলা",
    "চুদবাজ", "চুদখোর", "হারামজাদা", "হারামজাদী", "হারামি", "হারামী", "রান্ডি",
    "বাজে", "বোকাচোদা", "বোকাচুদি", "বোকাচোদ", "বেঙ্গাচুদা", "কুত্তা", "কুত্তি", 
    "মাদারচোদ", "শালা", "শালারবাচ্চা", "শালারপোলা", "শালারছেলে", "খানকি", 
    "খানকিরমেয়ে", "খানকিরছেলে", "খানকিরবাচ্চা", "বেশ্যা", "বেশ্যাকন্যা", 
    "বেশ্যারবাচ্চা", "মাগী", "মাগীরবাচ্চা", "মাগীরছেলে", "ডাইনী", "ডাইনি", 
    "হারামজাদারবাচ্চা", "হারামখোর", "কুত্তারবাচ্চা"
]

# Common spam/phishing patterns 
SPAM_DOMAINS = [
    "t.me/joinchat", "bit.ly", "goo.gl", "t.co", "whatsapp.com/join"
]