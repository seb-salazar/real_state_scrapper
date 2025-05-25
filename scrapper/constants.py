#    (?!["])(.*?)\n
# uncapitalize: (\w) -> \L$1
# space between words: \b\s+\b (\b is word boundary, \w includes the word)


cities = [
    "santiago",
    "conchali",
    "huechuraba",
    "independencia",
    "quilicura",
    "recoleta",
    "renca",
    "las-condes",
    "lo-barnechea",
    "providencia",
    "vitacura",
    "la-reina",
    "macul",
    "nunoa",
    "penalolen",
    "la-florida",
    "la-granja",
    "el-bosque",
    "la-cisterna",
    "san-ramon",
    "lo-espejo",
    "pedro-aguirre-cerda",
    "san-joaquin",
    "san-miguel",
    "cerrillos",
    "estacion-central",
    "maipu",
    "cerro-navia",
    "lo-prado",
    "pudahuel",
    "quinta-normal",
]

ONLY_PROYECTS_URL_FLAG = "_NoIndex_True"

APARTMENT_RESULT_GRID_ELEMENT = "poly-card__content"

CURRENCY_SYMBOL_CLASS = "andes-money-amount__currency-symbol"  # UF, $
AMOUNT_CLASS = "andes-money-amount__fraction"

# S3
BUCKET_NAME = "ss-real-state-ai"
