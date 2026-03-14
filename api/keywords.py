"""
Sakshyam Keyword Intelligence Database
Covers: Financial crime, narcotics, violence, cyber crime, conspiracy
Languages: English, Hindi, Marathi, Urdu (Roman script + Devanagari)
"""

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL: critical / high / medium / low
# Each entry: word → {level, meaning, ipc, category}
# ─────────────────────────────────────────────────────────────────────────────

KEYWORDS: dict[str, dict] = {

    # ══════════════════════════════
    # FINANCIAL CRIME
    # ══════════════════════════════
    "hawala":        {"level":"critical","meaning":"Illegal informal money transfer network","ipc":"PMLA §3&4 / FEMA §13","category":"financial"},
    "hundi":         {"level":"critical","meaning":"Hawala instrument — illegal money order","ipc":"PMLA §3 / FEMA §13","category":"financial"},
    "benami":        {"level":"critical","meaning":"Property held in false name — money laundering","ipc":"Benami Act §3 / PMLA §3","category":"financial"},
    "laundering":    {"level":"critical","meaning":"Money laundering","ipc":"PMLA §3&4","category":"financial"},
    "ransom":        {"level":"critical","meaning":"Ransom demand — kidnapping for money","ipc":"IPC §364A","category":"financial"},
    "extortion":     {"level":"critical","meaning":"Extortion","ipc":"IPC §383/384","category":"financial"},
    "bribe":         {"level":"critical","meaning":"Bribery — paying/receiving bribes","ipc":"IPC §171B / PC Act §7","category":"financial"},
    "kickback":      {"level":"high",    "meaning":"Illegal commission / kickback","ipc":"IPC §420 / PC Act §13","category":"financial"},
    "blackmail":     {"level":"critical","meaning":"Blackmail / criminal intimidation","ipc":"IPC §503/506","category":"financial"},
    "fraud":         {"level":"high",    "meaning":"Financial fraud","ipc":"IPC §420","category":"financial"},
    "forgery":       {"level":"high",    "meaning":"Document forgery","ipc":"IPC §463/468","category":"financial"},
    "counterfeit":   {"level":"critical","meaning":"Counterfeit currency / documents","ipc":"IPC §489A","category":"financial"},
    "fake":          {"level":"high",    "meaning":"Fake document or identity","ipc":"IPC §468 / IT Act §66C","category":"financial"},
    "scam":          {"level":"high",    "meaning":"Financial scam","ipc":"IPC §420","category":"financial"},
    "cheat":         {"level":"medium",  "meaning":"Cheating/fraud reference","ipc":"IPC §420","category":"financial"},
    "steal":         {"level":"high",    "meaning":"Theft reference","ipc":"IPC §379","category":"financial"},
    "theft":         {"level":"high",    "meaning":"Theft","ipc":"IPC §379","category":"financial"},
    "robbery":       {"level":"critical","meaning":"Robbery","ipc":"IPC §392","category":"financial"},
    "dacoity":       {"level":"critical","meaning":"Dacoity — gang robbery","ipc":"IPC §395","category":"financial"},

    # Hindi / Urdu financial
    "paisa":         {"level":"medium",  "meaning":"Money (Hindi)","ipc":"IPC §420","category":"financial"},
    "nakli":         {"level":"high",    "meaning":"Fake/counterfeit (Hindi)","ipc":"IPC §468/489A","category":"financial"},
    "ghapla":        {"level":"high",    "meaning":"Financial scam/fraud (Hindi)","ipc":"IPC §420","category":"financial"},
    "riswat":        {"level":"critical","meaning":"Bribe (Urdu/Hindi)","ipc":"PC Act §7","category":"financial"},
    "hisaab":        {"level":"medium",  "meaning":"Accounts/calculation — possible unaccounted funds","ipc":"IPC §420","category":"financial"},
    "udhaar":        {"level":"low",     "meaning":"Loan/debt — context dependent","ipc":"IPC §420","category":"financial"},

    # ══════════════════════════════
    # NARCOTICS / DRUGS
    # ══════════════════════════════
    "drug":          {"level":"critical","meaning":"Narcotic substance","ipc":"NDPS Act §20/21","category":"narcotics"},
    "drugs":         {"level":"critical","meaning":"Narcotic substances","ipc":"NDPS Act §20/21","category":"narcotics"},
    "narcotics":     {"level":"critical","meaning":"Narcotics","ipc":"NDPS Act §20","category":"narcotics"},
    "cocaine":       {"level":"critical","meaning":"Cocaine — Schedule I narcotic","ipc":"NDPS Act §21","category":"narcotics"},
    "heroin":        {"level":"critical","meaning":"Heroin — Schedule I narcotic","ipc":"NDPS Act §21","category":"narcotics"},
    "smack":         {"level":"critical","meaning":"Heroin slang","ipc":"NDPS Act §21","category":"narcotics"},
    "brown":         {"level":"high",    "meaning":"Heroin slang (brown sugar)","ipc":"NDPS Act §21","category":"narcotics"},
    "ganja":         {"level":"critical","meaning":"Cannabis — controlled substance","ipc":"NDPS Act §20","category":"narcotics"},
    "charas":        {"level":"critical","meaning":"Cannabis resin","ipc":"NDPS Act §20","category":"narcotics"},
    "cannabis":      {"level":"critical","meaning":"Cannabis — controlled substance","ipc":"NDPS Act §20","category":"narcotics"},
    "weed":          {"level":"high",    "meaning":"Cannabis (slang)","ipc":"NDPS Act §20","category":"narcotics"},
    "maal":          {"level":"high",    "meaning":"Contraband / drugs (slang)","ipc":"NDPS Act §20","category":"narcotics"},
    "powder":        {"level":"high",    "meaning":"Possible drug reference (powder narcotics)","ipc":"NDPS Act §21","category":"narcotics"},
    "tablet":        {"level":"medium",  "meaning":"Possible controlled substance pills","ipc":"NDPS Act §22","category":"narcotics"},
    "capsule":       {"level":"medium",  "meaning":"Possible controlled substance","ipc":"NDPS Act §22","category":"narcotics"},
    "mdma":          {"level":"critical","meaning":"MDMA — Schedule I controlled substance","ipc":"NDPS Act §22","category":"narcotics"},
    "ecstasy":       {"level":"critical","meaning":"MDMA/Ecstasy","ipc":"NDPS Act §22","category":"narcotics"},
    "supplier":      {"level":"high",    "meaning":"Drug supplier reference","ipc":"NDPS Act §29","category":"narcotics"},
    "peddler":       {"level":"critical","meaning":"Drug peddler","ipc":"NDPS Act §37","category":"narcotics"},
    "consignment":   {"level":"high",    "meaning":"Shipment — possible contraband","ipc":"Customs Act §135","category":"narcotics"},
    "parcel":        {"level":"medium",  "meaning":"Package — possible contraband","ipc":"Customs Act §135","category":"narcotics"},
    "smuggle":       {"level":"critical","meaning":"Smuggling reference","ipc":"Customs Act §135","category":"narcotics"},
    "smuggling":     {"level":"critical","meaning":"Smuggling","ipc":"Customs Act §135","category":"narcotics"},

    # ══════════════════════════════
    # VIOLENCE / THREATS
    # ══════════════════════════════
    "kill":          {"level":"critical","meaning":"Threat to kill","ipc":"IPC §302/307","category":"violence"},
    "murder":        {"level":"critical","meaning":"Murder reference","ipc":"IPC §302","category":"violence"},
    "shoot":         {"level":"critical","meaning":"Shooting / firearms reference","ipc":"IPC §307","category":"violence"},
    "shooting":      {"level":"critical","meaning":"Shooting incident","ipc":"IPC §307","category":"violence"},
    "bomb":          {"level":"critical","meaning":"Explosive device reference","ipc":"IPC §435/436 / UA(P)A","category":"violence"},
    "blast":         {"level":"critical","meaning":"Explosion reference","ipc":"IPC §435 / UA(P)A","category":"violence"},
    "explosion":     {"level":"critical","meaning":"Explosion","ipc":"IPC §435","category":"violence"},
    "attack":        {"level":"critical","meaning":"Attack/assault","ipc":"IPC §307","category":"violence"},
    "knife":         {"level":"high",    "meaning":"Bladed weapon","ipc":"IPC §324/326","category":"violence"},
    "stab":          {"level":"critical","meaning":"Stabbing reference","ipc":"IPC §324/326","category":"violence"},
    "gun":           {"level":"critical","meaning":"Firearm reference","ipc":"Arms Act §25","category":"violence"},
    "weapon":        {"level":"critical","meaning":"Weapon reference","ipc":"Arms Act §25","category":"violence"},
    "pistol":        {"level":"critical","meaning":"Pistol / handgun","ipc":"Arms Act §25","category":"violence"},
    "rifle":         {"level":"critical","meaning":"Rifle / long arm","ipc":"Arms Act §25","category":"violence"},
    "grenade":       {"level":"critical","meaning":"Grenade — explosive weapon","ipc":"Explosives Act / UA(P)A","category":"violence"},
    "hostage":       {"level":"critical","meaning":"Hostage-taking","ipc":"IPC §364A","category":"violence"},
    "kidnap":        {"level":"critical","meaning":"Kidnapping","ipc":"IPC §363/364","category":"violence"},
    "abduct":        {"level":"critical","meaning":"Abduction","ipc":"IPC §363","category":"violence"},
    "rape":          {"level":"critical","meaning":"Sexual assault reference","ipc":"IPC §376","category":"violence"},
    "assault":       {"level":"critical","meaning":"Physical assault","ipc":"IPC §351/354","category":"violence"},
    "beat":          {"level":"high",    "meaning":"Physical beating","ipc":"IPC §323/325","category":"violence"},
    "threat":        {"level":"high",    "meaning":"Criminal threat","ipc":"IPC §506","category":"violence"},
    "threaten":      {"level":"high",    "meaning":"Threatening someone","ipc":"IPC §506","category":"violence"},
    "intimidate":    {"level":"high",    "meaning":"Criminal intimidation","ipc":"IPC §503","category":"violence"},
    "eliminate":     {"level":"critical","meaning":"Eliminate — possible hit/murder order","ipc":"IPC §302/120B","category":"violence"},

    # Hindi violence
    "maar":          {"level":"critical","meaning":"Hit/kill (Hindi)","ipc":"IPC §302/307","category":"violence"},
    "maaro":         {"level":"critical","meaning":"Kill him/hit him (Hindi command)","ipc":"IPC §307","category":"violence"},
    "marta":         {"level":"critical","meaning":"Will kill (Hindi threat)","ipc":"IPC §506","category":"violence"},
    "supari":        {"level":"critical","meaning":"Contract killing — supari dena","ipc":"IPC §302/120B","category":"violence"},
    "khatam":        {"level":"critical","meaning":"Finish/eliminate (Hindi — threat)","ipc":"IPC §307","category":"violence"},
    "nikalo":        {"level":"high",    "meaning":"Remove/throw out — threat context","ipc":"IPC §506","category":"violence"},
    "dhamki":        {"level":"high",    "meaning":"Threat (Hindi)","ipc":"IPC §506","category":"violence"},
    "maar dalo":     {"level":"critical","meaning":"Kill them (Hindi)","ipc":"IPC §302","category":"violence"},

    # ══════════════════════════════
    # CYBER CRIME / IDENTITY FRAUD
    # ══════════════════════════════
    "hack":          {"level":"critical","meaning":"Hacking reference","ipc":"IT Act §66","category":"cyber"},
    "hacking":       {"level":"critical","meaning":"Computer hacking","ipc":"IT Act §66","category":"cyber"},
    "phishing":      {"level":"critical","meaning":"Phishing attack","ipc":"IT Act §66D","category":"cyber"},
    "malware":       {"level":"critical","meaning":"Malicious software","ipc":"IT Act §66","category":"cyber"},
    "ransomware":    {"level":"critical","meaning":"Ransomware attack","ipc":"IT Act §66","category":"cyber"},
    "password":      {"level":"high",    "meaning":"Credential reference — possible theft","ipc":"IT Act §66C","category":"cyber"},
    "account":       {"level":"medium",  "meaning":"Account reference — financial context","ipc":"IT Act §66C","category":"cyber"},
    "otp":           {"level":"high",    "meaning":"OTP sharing — possible SIM swap fraud","ipc":"IT Act §66C","category":"cyber"},
    "sim":           {"level":"high",    "meaning":"SIM card — possible SIM swap","ipc":"IT Act §66C","category":"cyber"},
    "aadhar":        {"level":"high",    "meaning":"Aadhaar reference — identity fraud risk","ipc":"IT Act §66C","category":"cyber"},
    "pan":           {"level":"high",    "meaning":"PAN card reference — identity fraud","ipc":"IT Act §66C","category":"cyber"},
    "identity":      {"level":"high",    "meaning":"Identity — possible theft/fraud","ipc":"IT Act §66C","category":"cyber"},
    "clone":         {"level":"critical","meaning":"Card cloning / identity cloning","ipc":"IT Act §66C","category":"cyber"},
    "darknet":       {"level":"critical","meaning":"Dark web reference","ipc":"IT Act §66","category":"cyber"},
    "darkweb":       {"level":"critical","meaning":"Dark web reference","ipc":"IT Act §66","category":"cyber"},
    "bitcoin":       {"level":"high",    "meaning":"Bitcoin — possible unregulated transaction","ipc":"IT Act §66","category":"cyber"},
    "crypto":        {"level":"high",    "meaning":"Cryptocurrency transaction","ipc":"IT Act §66","category":"cyber"},
    "wallet":        {"level":"medium",  "meaning":"Crypto wallet — possible illicit transfer","ipc":"IT Act §66C","category":"cyber"},

    # ══════════════════════════════
    # TERRORISM / EXTREMISM
    # ══════════════════════════════
    "terror":        {"level":"critical","meaning":"Terrorism reference","ipc":"UA(P)A §15","category":"terrorism"},
    "terrorist":     {"level":"critical","meaning":"Terrorist","ipc":"UA(P)A §15","category":"terrorism"},
    "jihad":         {"level":"critical","meaning":"Extremist militant reference","ipc":"UA(P)A §13","category":"terrorism"},
    "ied":           {"level":"critical","meaning":"Improvised Explosive Device","ipc":"UA(P)A / Explosives Act","category":"terrorism"},
    "sleeper":       {"level":"critical","meaning":"Sleeper cell reference","ipc":"UA(P)A §18","category":"terrorism"},
    "handler":       {"level":"high",    "meaning":"Handler — terrorist coordination","ipc":"UA(P)A §18","category":"terrorism"},
    "module":        {"level":"high",    "meaning":"Terror module reference","ipc":"UA(P)A §18","category":"terrorism"},
    "fidayeen":      {"level":"critical","meaning":"Suicide attacker","ipc":"UA(P)A §15","category":"terrorism"},

    # ══════════════════════════════
    # CONSPIRACY / EVASION
    # ══════════════════════════════
    "plan":          {"level":"medium",  "meaning":"Planning reference","ipc":"IPC §120B","category":"conspiracy"},
    "conspiracy":    {"level":"high",    "meaning":"Criminal conspiracy","ipc":"IPC §120A/120B","category":"conspiracy"},
    "escape":        {"level":"high",    "meaning":"Escape / flee reference","ipc":"IPC §224","category":"conspiracy"},
    "hide":          {"level":"medium",  "meaning":"Concealment reference","ipc":"IPC §201","category":"conspiracy"},
    "destroy":       {"level":"high",    "meaning":"Destroy evidence","ipc":"IPC §201","category":"conspiracy"},
    "dispose":       {"level":"high",    "meaning":"Dispose of evidence","ipc":"IPC §201","category":"conspiracy"},
    "delete":        {"level":"medium",  "meaning":"Delete data / evidence","ipc":"IT Act §66 / IPC §201","category":"conspiracy"},
    "clean":         {"level":"medium",  "meaning":"Clean up — possible evidence destruction","ipc":"IPC §201","category":"conspiracy"},
    "silent":        {"level":"medium",  "meaning":"Maintain silence — witness intimidation","ipc":"IPC §195A","category":"conspiracy"},
    "witness":       {"level":"medium",  "meaning":"Witness reference — possible tampering","ipc":"IPC §195A","category":"conspiracy"},
    "police":        {"level":"medium",  "meaning":"Police reference — possible evasion","ipc":"IPC §186","category":"conspiracy"},
    "arrest":        {"level":"high",    "meaning":"Arrest awareness — possible flight risk","ipc":"IPC §224","category":"conspiracy"},
    "run":           {"level":"medium",  "meaning":"Flight/escape reference","ipc":"IPC §224","category":"conspiracy"},
    "border":        {"level":"high",    "meaning":"Border crossing — possible illegal movement","ipc":"Passport Act §12","category":"conspiracy"},
    "crossing":      {"level":"high",    "meaning":"Border/illegal crossing","ipc":"Passport Act §12","category":"conspiracy"},
    "contact":       {"level":"low",     "meaning":"Contact reference","ipc":"IPC §120B","category":"conspiracy"},
    "meeting":       {"level":"low",     "meaning":"Meeting reference — context dependent","ipc":"IPC §120B","category":"conspiracy"},
    "signal":        {"level":"medium",  "meaning":"Signal/code — possible coordination","ipc":"IPC §120B","category":"conspiracy"},
    "code":          {"level":"medium",  "meaning":"Code word — possible criminal coordination","ipc":"IPC §120B","category":"conspiracy"},

    # Hindi conspiracy
    "setting":       {"level":"high",    "meaning":"Arrangement/fixing (crime slang)","ipc":"IPC §120B","category":"conspiracy"},
    "jugaad":        {"level":"high",    "meaning":"Illegal workaround/fix","ipc":"IPC §120B","category":"conspiracy"},
    "kaam":          {"level":"medium",  "meaning":"Work/job — context dependent","ipc":"IPC §120B","category":"conspiracy"},
    "dhanda":        {"level":"high",    "meaning":"Criminal business (slang)","ipc":"IPC §420","category":"conspiracy"},
    "baat":          {"level":"low",     "meaning":"Talk/discussion","ipc":"IPC §120B","category":"conspiracy"},
    "khabar":        {"level":"medium",  "meaning":"Information / tip-off","ipc":"IPC §201","category":"conspiracy"},
    "saboot":        {"level":"medium",  "meaning":"Evidence (Hindi) — possible destruction","ipc":"IPC §201","category":"conspiracy"},
    "pakad":         {"level":"high",    "meaning":"Catch/arrest (Hindi) — awareness of police","ipc":"IPC §224","category":"conspiracy"},
    "bachao":        {"level":"high",    "meaning":"Save/escape (Hindi)","ipc":"IPC §224","category":"conspiracy"},
    "nikal":         {"level":"high",    "meaning":"Get out/escape (Hindi)","ipc":"IPC §224","category":"conspiracy"},
    "bhaag":         {"level":"critical","meaning":"Run/flee (Hindi)","ipc":"IPC §224","category":"conspiracy"},
    "chhupa":        {"level":"high",    "meaning":"Hide (Hindi)","ipc":"IPC §201","category":"conspiracy"},

    # ══════════════════════════════
    # MONEY / TRANSFERS
    # ══════════════════════════════
    "transfer":      {"level":"high",    "meaning":"Money transfer — possible hawala","ipc":"PMLA §3","category":"financial"},
    "cash":          {"level":"medium",  "meaning":"Cash transaction — unaccounted","ipc":"PMLA §3","category":"financial"},
    "lakh":          {"level":"medium",  "meaning":"Large cash amount (₹1L+)","ipc":"PMLA §3","category":"financial"},
    "crore":         {"level":"high",    "meaning":"Very large sum (₹1Cr+) — laundering risk","ipc":"PMLA §3&4","category":"financial"},
    "deposit":       {"level":"medium",  "meaning":"Deposit — possible structured transaction","ipc":"PMLA §3","category":"financial"},
    "withdraw":      {"level":"medium",  "meaning":"Withdrawal — possible illicit cash-out","ipc":"PMLA §3","category":"financial"},
    "account":       {"level":"medium",  "meaning":"Bank account","ipc":"IPC §420","category":"financial"},
    "payment":       {"level":"medium",  "meaning":"Payment reference","ipc":"IPC §420","category":"financial"},
    "wire":          {"level":"high",    "meaning":"Wire transfer — possible offshore","ipc":"FEMA §13","category":"financial"},
    "offshore":      {"level":"critical","meaning":"Offshore account — foreign asset concealment","ipc":"FEMA §13 / PMLA §3","category":"financial"},
    "shell":         {"level":"critical","meaning":"Shell company reference","ipc":"PMLA §3","category":"financial"},
}

# Color map by level
LEVEL_COLORS = {
    "critical": "#ef4444",
    "high":     "#f97316",
    "medium":   "#f59e0b",
    "low":      "#84cc16",
}

# Category labels
CATEGORY_LABELS = {
    "financial":   "Financial Crime",
    "narcotics":   "Narcotics / Drugs",
    "violence":    "Violence / Threats",
    "cyber":       "Cyber Crime",
    "terrorism":   "Terrorism / Extremism",
    "conspiracy":  "Conspiracy / Evasion",
}

# Common stopwords to exclude from word frequency (multi-language)
STOPWORDS = {
    # English
    "the","and","for","are","but","not","you","all","can","was","had","has",
    "have","this","that","with","from","they","will","been","were","his","her",
    "their","said","what","when","who","how","its","our","there","than","then",
    "also","into","over","more","just","your","him","get","got","did","out",
    "about","would","could","should","one","two","three","four","five","six",
    "seven","eight","nine","ten","yes","no","okay","ok","hello","hey",
    # Hindi stopwords (roman)
    "aur","hai","hain","tha","thi","the","kya","kar","karo","karo","nahi",
    "nhi","mein","main","mujhe","muje","tumhe","aap","apne","apna","iske",
    "uske","woh","wahi","yeh","yahi","iske","uska","unka","inka","lekin",
    "par","per","toh","bhi","koi","kuch","sab","sirf","abhi","phir","fir",
    "bahut","zyada","thoda","accha","theek","hoga","hogi","hoge","gaya","gayi",
    "aaya","aayi","jao","jao","raho","raha","rahi","rahe","liya","liye","diya",
    "diye","hua","hui","hue","leke","leke","dekho","dekh","bolo","bolo","suno",
    # Marathi
    "ahe","nahi","kay","tar","pan","mhanje","tyala","tila","amhi","tumhi",
    "aahe","naste","asto","aste","basla","basli","gela","geli","kela","keli",
}
