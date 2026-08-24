import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = Path(__file__).with_name("kidslearn.db")

STORIES = [
    ("Le petit nuage courageux","The Brave Little Cloud","Débutant","Aventure",5,"☁️","Petit Nuage avait peur de quitter la montagne. Un matin, il respira profondément et partit découvrir la vallée. Il rencontra des oiseaux, des fleurs et une rivière brillante. Petit Nuage comprit que le courage signifie essayer malgré la peur.","Little Cloud was afraid to leave the mountain. One morning, he took a deep breath and discovered the valley. He met birds, flowers and a sparkling river. Little Cloud learned that courage means trying even when you are afraid."),
    ("Mina et le livre magique","Mina and the Magic Book","Intermédiaire","Fantastique",7,"📚","Mina trouva un livre ancien. Quand elle ouvrit la première page, les lettres se mirent à danser. Le livre lui demanda de trouver trois mots gentils à offrir à ses amis.","Mina found an old book. When she opened the first page, the letters began to dance. The book asked her to find three kind words for her friends."),
    ("Le secret de la forêt","The Secret of the Forest","Avancé","Mystère",9,"🌳","Noah suivit une petite lumière entre les arbres. Il découvrit une porte couverte de symboles. Pour l'ouvrir, il devait lire un message et résoudre une énigme.","Noah followed a tiny light through the trees. He discovered a door covered with symbols. To open it, he had to read a message and solve a riddle."),
    ("Lila apprend les sons","Lila Learns Sounds","Débutant","Alphabétisation",4,"🔤","Lila jouait avec les lettres. Elle trouva A dans ami, B dans ballon et C dans chat. En répétant les sons, elle réussit à lire de petits mots.","Lila played with letters. She found A in ami, B in ballon and C in chat. By repeating sounds, she learned to read small words."),
    ("Tom et les syllabes","Tom and the Syllables","Débutant","Syllabes",5,"🧩","Tom découvrit que les mots pouvaient être découpés en petits morceaux. MA, MI, MO puis MA-MA. En jouant avec les syllabes, il forma de nouveaux mots.","Tom discovered that words could be split into small parts. MA, MI, MO and then MA-MA. By playing with syllables, he built new words."),
    ("Awa et le ballon rouge","Awa and the Red Ball","Débutant","Aventure",4,"🔴","Awa jouait avec son ballon rouge. Le vent l'emporta près d'un arbre. Elle suivit le ballon et retrouva son ami Sami, qui l'aida à le récupérer.","Awa played with her red ball. The wind carried it near a tree. She followed it and found her friend Sami, who helped her get it back."),
    ("Le jardin des couleurs","The Garden of Colors","Débutant","Découverte",5,"🌈","Nina visita un jardin. Elle vit une fleur rouge, une feuille verte et un papillon jaune. Elle apprit à nommer les couleurs en jouant.","Nina visited a garden. She saw a red flower, a green leaf and a yellow butterfly. She learned to name colors while playing."),
    ("Bobo le petit singe","Bobo the Little Monkey","Débutant","Animaux",5,"🐒","Bobo aimait sauter de branche en branche. Un jour, il aida un petit oiseau à retrouver son nid. Tous les animaux le remercièrent.","Bobo loved jumping from branch to branch. One day, he helped a little bird find its nest. All the animals thanked him."),
    ("Le vélo de Sami","Sami's Bicycle","Débutant","Vie quotidienne",5,"🚲","Sami apprit à faire du vélo. Au début, il tomba doucement. Son papa l'encouragea. Après plusieurs essais, Sami roula tout seul.","Sami learned to ride a bicycle. At first, he fell gently. His father encouraged him. After several tries, Sami rode alone."),
    ("La petite étoile","The Little Star","Débutant","Fantastique",4,"⭐","Une petite étoile voulait briller plus fort. Elle découvrit qu'elle éclairait déjà le chemin d'un enfant qui rentrait chez lui.","A little star wanted to shine brighter. She discovered that she was already lighting the way for a child going home."),
    ("Le marché de couleurs","The Colorful Market","Intermédiaire","Découverte",7,"🛍️","Yara accompagna sa maman au marché. Elle compta trois mangues, deux bananes et quatre oranges. Elle apprit à comparer les quantités.","Yara went to the market with her mother. She counted three mangoes, two bananas and four oranges. She learned to compare quantities."),
    ("Kofi et la rivière","Kofi and the River","Intermédiaire","Nature",8,"🌊","Kofi voulait traverser une rivière. Il observa le courant, choisit un passage calme et demanda de l'aide à son grand frère. Ensemble, ils traversèrent en sécurité.","Kofi wanted to cross a river. He watched the current, chose a calm place and asked his older brother for help. Together, they crossed safely."),
    ("Le robot qui aimait lire","The Robot Who Loved Reading","Intermédiaire","Technologie",7,"🤖","Riko était un petit robot qui apprenait à lire. Chaque soir, il lisait une nouvelle page. Il découvrit que les livres pouvaient lui apprendre de nouveaux mots et de nouvelles idées.","Riko was a little robot learning to read. Every evening, he read a new page. He discovered that books could teach him new words and new ideas."),
    ("Aïcha et la graine","Aisha and the Seed","Intermédiaire","Nature",6,"🌱","Aïcha planta une graine dans un pot. Elle l'arrosa chaque matin et plaça le pot près de la lumière. Quelques jours plus tard, une petite pousse apparut.","Aisha planted a seed in a pot. She watered it every morning and placed it near the light. A few days later, a small sprout appeared."),
    ("Le trésor de la plage","The Beach Treasure","Intermédiaire","Aventure",8,"🏖️","Lucas trouva une petite boîte sur la plage. À l'intérieur, il y avait une carte, un coquillage et un message. La carte le conduisit vers un rocher où il trouva un trésor: un livre.","Lucas found a small box on the beach. Inside were a map, a shell and a message. The map led him to a rock where he found a treasure: a book."),
    ("Nora et les mots nouveaux","Nora and New Words","Intermédiaire","Vocabulaire",6,"📝","Nora gardait un carnet de mots. Chaque jour, elle écrivait trois nouveaux mots et inventait une phrase avec chacun. Son vocabulaire grandissait rapidement.","Nora kept a word notebook. Each day, she wrote three new words and made a sentence with each one. Her vocabulary grew quickly."),
    ("Le village sans couleurs","The Colorless Village","Avancé","Mystère",10,"🎨","Un matin, le village de Léo devint tout gris. Avec ses amis, il chercha la cause du problème. Ils découvrirent qu'une vieille machine avait mélangé les couleurs. Ils la réparèrent ensemble.","One morning, Leo's village became completely gray. With his friends, he searched for the cause. They discovered an old machine had mixed the colors. They repaired it together."),
    ("Le message des étoiles","The Message from the Stars","Avancé","Science",10,"🔭","Sara observait le ciel avec un petit télescope. Elle nota les positions des étoiles et remarqua un motif. Son professeur lui expliqua comment les scientifiques utilisent l'observation pour poser des questions.","Sara watched the sky with a small telescope. She recorded star positions and noticed a pattern. Her teacher explained how scientists use observation to ask questions."),
    ("Le pont des amis","The Friends' Bridge","Avancé","Valeurs",9,"🌉","Deux villages étaient séparés par une rivière. Les enfants imaginèrent un pont en bois. Les adultes les aidèrent à construire un passage solide qui rapprocha les deux communautés.","Two villages were separated by a river. The children imagined a wooden bridge. Adults helped them build a strong crossing that brought the communities closer."),
    ("Le code secret de Zoé","Zoe's Secret Code","Avancé","Logique",9,"🔐","Zoé reçut une lettre avec un code. Elle observa les répétitions, regroupa les symboles et comprit le message. Elle avait découvert une énigme qui demandait patience et logique.","Zoe received a letter with a code. She studied repetitions, grouped the symbols and understood the message. She had solved a puzzle that required patience and logic."),
]

QUESTIONS = [
    (1,"Pourquoi Petit Nuage est-il parti ?","Why did Little Cloud leave?","Pour découvrir la vallée","To discover the valley","Pour dormir","To sleep","Pour construire une maison","To build a house","A","compréhension"),
    (2,"Que faisait le livre quand Mina l'a ouvert ?","What did the book do when Mina opened it?","Les lettres dansaient","The letters danced","Le livre chantait","The book sang","La porte s'ouvrait","The door opened","A","compréhension"),
    (3,"Que devait faire Noah pour ouvrir la porte ?","What did Noah have to do to open the door?","Lire un message et résoudre une énigme","Read a message and solve a riddle","Dormir sous un arbre","Sleep under a tree","Chanter","Sing","A","compréhension"),
    (4,"Quelle lettre trouve-t-elle dans ballon ?","Which letter does she find in ballon?","B","B","A","A","D","D","A","lettres"),
    (5,"Quel mot peut être formé avec MA + MA ?","What word can be formed with MA + MA?","MAMA","MAMA","TOTO","TOTO","LILI","LILI","A","syllabes"),
    (6,"De quelle couleur est le ballon d'Awa ?","What color is Awa's ball?","Rouge","Red","Vert","Green","Bleu","Blue","A","compréhension"),
    (7,"Quelle couleur a le papillon ?","What color is the butterfly?","Jaune","Yellow","Noir","Black","Rose","Pink","A","vocabulaire"),
    (8,"Qui Bobo aide-t-il ?","Who does Bobo help?","Un petit oiseau","A little bird","Un poisson","A fish","Un chien","A dog","A","compréhension"),
    (9,"Que fait Sami à la fin ?","What does Sami do at the end?","Il roule tout seul","He rides alone","Il dort","He sleeps","Il nage","He swims","A","compréhension"),
    (10,"Que voulait la petite étoile ?","What did the little star want?","Briller plus fort","Shine brighter","Dormir","Sleep","Tomber","Fall","A","compréhension"),
    (11,"Combien de mangues Yara compte-t-elle ?","How many mangoes does Yara count?","Trois","Three","Deux","Two","Quatre","Four","A","nombres"),
    (12,"Comment Kofi choisit-il le passage ?","How does Kofi choose the crossing?","Il observe le courant","He watches the current","Il ferme les yeux","He closes his eyes","Il court sans regarder","He runs without looking","A","compréhension"),
    (13,"Que fait Riko chaque soir ?","What does Riko do every evening?","Il lit une page","He reads a page","Il danse","He dances","Il cuisine","He cooks","A","lecture"),
    (14,"Que fait Aïcha chaque matin ?","What does Aisha do every morning?","Elle arrose la graine","She waters the seed","Elle coupe la plante","She cuts the plant","Elle vend le pot","She sells the pot","A","compréhension"),
    (15,"Quel est le trésor de Lucas ?","What is Lucas's treasure?","Un livre","A book","Une pièce d'or","A gold coin","Un bateau","A boat","A","compréhension"),
    (16,"Combien de mots Nora écrit-elle chaque jour ?","How many words does Nora write each day?","Trois","Three","Un","One","Dix","Ten","A","nombres"),
    (17,"Pourquoi le village de Léo est-il devenu gris ?","Why did Leo's village become gray?","Une machine avait mélangé les couleurs","A machine had mixed the colors","Il a plu","It rained","Les habitants ont déménagé","The people moved away","A","compréhension"),
    (18,"Avec quoi Sara observe-t-elle le ciel ?","What does Sara use to observe the sky?","Un télescope","A telescope","Une loupe","A magnifying glass","Un microscope","A microscope","A","science"),
    (19,"Que construisent les villages ?","What do the villages build?","Un pont","A bridge","Une école","A school","Une tour","A tower","A","compréhension"),
    (20,"Que demande le code secret de Zoé ?","What does Zoe's secret code require?","Patience et logique","Patience and logic","Force et vitesse","Strength and speed","Chance","Luck","A","logique"),
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,role TEXT NOT NULL CHECK(role IN ('parent','child','admin'))
    );
    CREATE TABLE IF NOT EXISTS children(
      id INTEGER PRIMARY KEY AUTOINCREMENT,parent_id INTEGER NOT NULL,name TEXT NOT NULL,
      age INTEGER NOT NULL,level TEXT NOT NULL,avatar TEXT DEFAULT '🧒',
      FOREIGN KEY(parent_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS stories(
      id INTEGER PRIMARY KEY AUTOINCREMENT,title_fr TEXT NOT NULL,title_en TEXT NOT NULL,
      level TEXT NOT NULL,category TEXT NOT NULL,minutes INTEGER NOT NULL,emoji TEXT NOT NULL,
      text_fr TEXT NOT NULL,text_en TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS questions(
      id INTEGER PRIMARY KEY AUTOINCREMENT,story_id INTEGER NOT NULL,prompt_fr TEXT NOT NULL,prompt_en TEXT NOT NULL,
      option_a_fr TEXT NOT NULL,option_a_en TEXT NOT NULL,option_b_fr TEXT NOT NULL,option_b_en TEXT NOT NULL,
      option_c_fr TEXT NOT NULL,option_c_en TEXT NOT NULL,answer TEXT NOT NULL,skill TEXT NOT NULL,
      FOREIGN KEY(story_id) REFERENCES stories(id)
    );
    CREATE TABLE IF NOT EXISTS results(
      id INTEGER PRIMARY KEY AUTOINCREMENT,child_id INTEGER NOT NULL,story_id INTEGER NOT NULL,
      score INTEGER NOT NULL,total INTEGER NOT NULL,percentage INTEGER NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(child_id) REFERENCES children(id),FOREIGN KEY(story_id) REFERENCES stories(id)
    );
    CREATE TABLE IF NOT EXISTS badges(
      id INTEGER PRIMARY KEY AUTOINCREMENT,code TEXT UNIQUE NOT NULL,name_fr TEXT NOT NULL,name_en TEXT NOT NULL,
      icon TEXT NOT NULL,description_fr TEXT NOT NULL,description_en TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS child_badges(
      child_id INTEGER NOT NULL,badge_id INTEGER NOT NULL,earned_at TEXT DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(child_id,badge_id),FOREIGN KEY(child_id) REFERENCES children(id),FOREIGN KEY(badge_id) REFERENCES badges(id)
    );
    """)
    # Ajoute les histoires manquantes sans supprimer les données existantes.
    for story in STORIES:
        exists = conn.execute("SELECT id FROM stories WHERE title_fr=?", (story[0],)).fetchone()
        if not exists:
            conn.execute("""INSERT INTO stories
              (title_fr,title_en,level,category,minutes,emoji,text_fr,text_en) VALUES(?,?,?,?,?,?,?,?)""", story)

    # Ajoute une question pour chaque histoire manquante. Les IDs des histoires
    # sont recherchés par titre afin de fonctionner même avec une ancienne base.
    question_count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    if question_count < len(QUESTIONS):
        for q in QUESTIONS:
            story_id = conn.execute("SELECT id FROM stories WHERE id=?", (q[0],)).fetchone()
            if story_id:
                exists = conn.execute("SELECT id FROM questions WHERE story_id=?", (q[0],)).fetchone()
                if not exists:
                    conn.execute("""INSERT INTO questions
                      (story_id,prompt_fr,prompt_en,option_a_fr,option_a_en,option_b_fr,option_b_en,
                       option_c_fr,option_c_en,answer,skill) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", q)
    badges = [
      ("first_story","Première histoire","First story","🌱","Tu as terminé ta première histoire !","You finished your first story!"),
      ("five_stories","Lecteur en herbe","Rising reader","📚","Cinq activités terminées.","Five activities completed."),
      ("perfect","Score parfait","Perfect score","🏆","Un défi avec 100 % !","A challenge with 100%!"),
      ("bilingual","Petit polyglotte","Little polyglot","🌍","Tu explores le français et l'anglais.","You explore French and English.")
    ]
    conn.executemany("""INSERT OR IGNORE INTO badges(code,name_fr,name_en,icon,description_fr,description_en)
                        VALUES(?,?,?,?,?,?)""", badges)
    # Compte administrateur local pour le prototype.
    # Il est créé automatiquement si absent, même lorsque l'application est
    # lancée avec `flask run` (et pas seulement avec `python app.py`).
    admin_email = "admin@kidslearn.local"
    admin_password = "Admin123!"
    existing_admin = conn.execute(
        "SELECT id FROM users WHERE email=? AND role='admin'",
        (admin_email,)
    ).fetchone()
    if not existing_admin:
        conn.execute(
            "INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,?)",
            ("KidsLearn Admin", admin_email, generate_password_hash(admin_password), "admin")
        )
    conn.commit()
    conn.close()

def create_user(name,email,password,role="parent"):
    conn=get_db()
    try:
        cur=conn.execute("INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,?)",
                         (name,email,generate_password_hash(password),role))
        conn.commit(); return cur.lastrowid
    except sqlite3.IntegrityError: return None
    finally: conn.close()

def verify_user(email,password):
    conn=get_db(); row=conn.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone(); conn.close()
    if row and check_password_hash(row["password_hash"],password):
        return {"user_id":row["id"],"name":row["name"],"role":row["role"]}
    return None

def create_child(parent_id,name,age,level,avatar="🧒"):
    conn=get_db()
    cur=conn.execute("INSERT INTO children(parent_id,name,age,level,avatar) VALUES(?,?,?,?,?)",
                     (parent_id,name,age,level,avatar))
    conn.commit(); cid=cur.lastrowid; conn.close(); return cid

def get_children_for_parent(parent_id):
    conn=get_db()
    rows=conn.execute("""SELECT c.*,COALESCE(ROUND(AVG(r.percentage)),0) progress,
                         COUNT(r.id) completed FROM children c LEFT JOIN results r ON r.child_id=c.id
                         WHERE c.parent_id=? GROUP BY c.id ORDER BY c.id DESC""",(parent_id,)).fetchall()
    conn.close(); return [dict(r) for r in rows]

def get_parent_summary(parent_id):
    conn=get_db()
    row=conn.execute("""SELECT COUNT(DISTINCT c.id) children,COUNT(r.id) activities,
                        COALESCE(ROUND(AVG(r.percentage)),0) average
                        FROM children c LEFT JOIN results r ON r.child_id=c.id WHERE c.parent_id=?""",(parent_id,)).fetchone()
    conn.close(); return dict(row)

def get_child_by_id(child_id):
    conn=get_db(); row=conn.execute("SELECT * FROM children WHERE id=?",(child_id,)).fetchone(); conn.close()
    return dict(row) if row else None

def get_stories(level=None):
    conn=get_db()
    rows=conn.execute("SELECT * FROM stories "+("WHERE level=? " if level else "")+"ORDER BY id",
                      (level,) if level else ()).fetchall()
    conn.close(); return [dict(r) for r in rows]

def get_story(story_id):
    conn=get_db(); row=conn.execute("SELECT * FROM stories WHERE id=?",(story_id,)).fetchone(); conn.close()
    return dict(row) if row else None

def get_questions(story_id):
    conn=get_db(); rows=conn.execute("SELECT * FROM questions WHERE story_id=?",(story_id,)).fetchall(); conn.close()
    return [dict(r) for r in rows]

def save_result(child_id,story_id,score,total,percentage):
    conn=get_db(); conn.execute("""INSERT INTO results(child_id,story_id,score,total,percentage)
                                   VALUES(?,?,?,?,?)""",(child_id,story_id,score,total,percentage)); conn.commit()
    _award_badges(conn,child_id); conn.commit(); conn.close()

def _award_badges(conn,child_id):
    count=conn.execute("SELECT COUNT(*) FROM results WHERE child_id=?",(child_id,)).fetchone()[0]
    if count>=1: _give(conn,child_id,"first_story")
    if count>=5: _give(conn,child_id,"five_stories")
    if conn.execute("SELECT 1 FROM results WHERE child_id=? AND percentage=100",(child_id,)).fetchone(): _give(conn,child_id,"perfect")

def _give(conn,child_id,code):
    row=conn.execute("SELECT id FROM badges WHERE code=?",(code,)).fetchone()
    if row: conn.execute("INSERT OR IGNORE INTO child_badges(child_id,badge_id) VALUES(?,?)",(child_id,row["id"]))

def get_child_progress(child_id):
    conn=get_db()
    rows=conn.execute("""SELECT r.*,s.title_fr,s.title_en,s.level,s.category
                         FROM results r JOIN stories s ON s.id=r.story_id
                         WHERE r.child_id=? ORDER BY r.created_at DESC""",(child_id,)).fetchall()
    conn.close(); return [dict(r) for r in rows]

def get_child_badges(child_id):
    conn=get_db()
    rows=conn.execute("""SELECT b.*,cb.earned_at FROM child_badges cb JOIN badges b ON b.id=cb.badge_id
                         WHERE cb.child_id=? ORDER BY cb.earned_at DESC""",(child_id,)).fetchall()
    conn.close(); return [dict(r) for r in rows]

def get_skill_progress(child_id):
    conn=get_db()
    rows=conn.execute("""SELECT q.skill,ROUND(AVG(CASE WHEN q.answer = x.chosen THEN 100.0 ELSE 0 END)) score
                         FROM questions q JOIN (
                           SELECT q2.id,q2.answer,COALESCE(r.percentage,0) AS result_score,
                                  CASE WHEN r.percentage>=50 THEN q2.answer ELSE '' END chosen
                           FROM questions q2 LEFT JOIN results r ON r.story_id=q2.story_id AND r.child_id=?
                         ) x ON x.id=q.id GROUP BY q.skill""",(child_id,)).fetchall()
    # Simpler and more reliable skill indicator based on completed story results.
    rows2=conn.execute("""SELECT s.category skill,ROUND(AVG(r.percentage)) score
                          FROM results r JOIN stories s ON s.id=r.story_id
                          WHERE r.child_id=? GROUP BY s.category""",(child_id,)).fetchall()
    conn.close(); return [dict(r) for r in rows2]

def get_admin_summary():
    conn=get_db()
    summary=conn.execute("""SELECT
      (SELECT COUNT(*) FROM users WHERE role='parent') parents,
      (SELECT COUNT(*) FROM children) children,
      (SELECT COUNT(*) FROM stories) stories,
      (SELECT COUNT(*) FROM results) assessments,
      COALESCE((SELECT ROUND(AVG(percentage)) FROM results),0) average""").fetchone()
    recent=conn.execute("""SELECT r.*,c.name child_name,s.title_fr story FROM results r
                           JOIN children c ON c.id=r.child_id JOIN stories s ON s.id=r.story_id
                           ORDER BY r.created_at DESC LIMIT 10""").fetchall()
    conn.close(); return dict(summary),[dict(x) for x in recent]
