CREATE TABLE IF NOT EXISTS TickerDeCaisseTypeEnum (
    name TEXT NOT NULL PRIMARY KEY,
    required BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS ItemArticleCategorieEnum (
    name TEXT NOT NULL PRIMARY KEY,
    required BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS ItemArticleGroupeEnum (
    name TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS ItemArticleStruct (
    id INTEGER NOT NULL,
    ident TEXT NOT NULL,
    prix FLOAT NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    group TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(category) REFERENCES ItemArticleCategorieEnum(name) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ArticleStruct (
    id INTEGER NOT NULL,
    item INTEGER NOT NULL,
    remise FLOAT NOT NULL DEFAULT 0.0,
    quantity INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (id, item, remise, quantity),
    FOREIGN KEY(item) REFERENCES ItemArticleStruct(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS TicketDeCaisseStruct (
    id INTEGER PRIMARY KEY,
    shop TEXT NOT NULL,
    localisation TEXT NOT NULL,
    date DATE NOT NULL,
    articles INTEGER,
    category TEXT NOT NULL,
    FOREIGN KEY(articles) REFERENCES ArticleStruct(id) ON DELETE SET NULL,
    FOREIGN KEY(category) REFERENCES TickerDeCaisseTypeEnum(name) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS DatabaseRowStruct (
    id INTEGER PRIMARY KEY,
    shop TEXT NOT NULL,
    localisation TEXT NOT NULL,
    category TEXT NOT NULL,
    itemArticleCategorie TEXT NOT NULL,
    itemArticle TEXT NOT NULL,
    itemNomArticle TEXT NOT NULL,
    prix TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS FeuilleStruct (
    date INTEGER PRIMARY KEY NOT NULL,
    factures TEXT NOT NULL DEFAULT "{}"
);