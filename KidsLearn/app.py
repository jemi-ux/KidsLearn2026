from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import *
from ai_assistant import assistant_message

app=Flask(__name__)
app.secret_key="kidslearn-dev-secret-change-me"
LANGS={"fr":"Français","en":"English"}

init_db()

@app.context_processor
def globals():
    return {"current_lang":session.get("lang","fr"),"langs":LANGS,"user":session.get("user")}

@app.route("/")
def index(): return render_template("index.html")

@app.post("/set-language")
def set_language():
    lang=request.form.get("lang","fr")
    if lang in LANGS: session["lang"]=lang
    return redirect(request.referrer or url_for("index"))

@app.route("/register/parent",methods=["GET","POST"])
def register_parent():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
        if not name or not email or len(password)<6: flash("Veuillez remplir tous les champs. Mot de passe : 6 caractères minimum.","error")
        elif create_user(name,email,password,"parent"):
            flash("Compte créé. Vous pouvez vous connecter.","success"); return redirect(url_for("login"))
        else: flash("Cette adresse e-mail est déjà utilisée.","error")
    return render_template("register_parent.html")

@app.route("/register/child",methods=["GET","POST"])
def register_child():
    if session.get("role")!="parent": return redirect(url_for("login"))
    if request.method=="POST":
        name=request.form.get("name","").strip(); age=request.form.get("age",type=int); level=request.form.get("level","Débutant"); avatar=request.form.get("avatar","🧒")
        if name and age: create_child(session["user_id"],name,age,level,avatar); flash("Profil enfant ajouté !","success"); return redirect(url_for("parent_dashboard"))
        flash("Informations invalides.","error")
    return render_template("register_child.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=verify_user(request.form.get("email","").strip().lower(),request.form.get("password",""))
        if u: session["user"]=u; session.update(u); return redirect(url_for("admin_dashboard" if u["role"]=="admin" else "parent_dashboard" if u["role"]=="parent" else "child_dashboard",**({"child_id":u["user_id"]} if u["role"]=="child" else {})))
        flash("E-mail ou mot de passe incorrect.","error")
    return render_template("login.html")

@app.get("/logout")
def logout(): session.clear(); return redirect(url_for("index"))

@app.get("/parent")
def parent_dashboard():
    if session.get("role")!="parent": return redirect(url_for("login"))
    return render_template("parent_dashboard.html",children=get_children_for_parent(session["user_id"]),summary=get_parent_summary(session["user_id"]))

@app.get("/child/<int:child_id>")
def child_dashboard(child_id):
    child=get_child_by_id(child_id)
    if not child: return redirect(url_for("login"))
    if session.get("role")=="parent" and child["parent_id"]!=session["user_id"]: return redirect(url_for("parent_dashboard"))
    if session.get("role")=="child" and session.get("user_id")!=child_id: return redirect(url_for("login"))
    progress=get_child_progress(child_id)
    return render_template("child_dashboard.html",child=child,stories=get_stories(child["level"]),progress=progress,badges=get_child_badges(child_id),skills=get_skill_progress(child_id))

@app.post("/api/ai/feedback")
def ai_feedback():
    level=request.form.get("level", "").strip()
    liked=request.form.get("liked")
    if liked not in {"yes", "some", "no"}: liked=None
    session["kidslearn_level"] = level
    if liked: session["kidslearn_liked"] = liked
    return jsonify({"message":assistant_message(level, liked, session.get("lang","fr"))})

@app.get("/library")
def library():
    level=request.args.get("level", "").strip()
    category=request.args.get("category", "").strip()
    stories=get_stories(level or None)
    if category:
        stories=[s for s in stories if s["category"]==category]
    categories=sorted({s["category"] for s in get_stories()})
    return render_template("bibliothèque.html", stories=stories, selected_level=level, selected_category=category, categories=categories)

@app.get("/story/<int:story_id>")
def story(story_id):
    item=get_story(story_id)
    if not item: return redirect(url_for("library"))
    return render_template("story.html",story=item,questions=get_questions(story_id))

@app.post("/assessment/<int:story_id>")
def assessment(story_id):
    child_id=request.form.get("child_id",type=int)
    questions=get_questions(story_id); score=0
    for q in questions:
        if request.form.get(f"q_{q['id']}")==q["answer"]: score+=1
    total=len(questions); percentage=round(score/total*100) if total else 0
    if child_id and get_child_by_id(child_id): save_result(child_id,story_id,score,total,percentage)
    return render_template("result.html",score=score,total=total,percentage=percentage,story=get_story(story_id),child_id=child_id)

@app.get("/games")
def games():
    return render_template("games.html")

@app.get("/admin")
def admin_dashboard():
    if session.get("role")!="admin": return redirect(url_for("login"))
    summary,recent=get_admin_summary()
    return render_template("admin_dashboard.html",summary=summary,recent=recent)

@app.get("/api/progress/<int:child_id>")
def api_progress(child_id): return jsonify({"progress":get_child_progress(child_id),"badges":get_child_badges(child_id),"skills":get_skill_progress(child_id)})

if __name__=="__main__":
    app.run(debug=True)
