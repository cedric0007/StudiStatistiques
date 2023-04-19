# http://127.0.0.1:8000/docs
# https://fastapi.tiangolo.com/tutorial/security/first-steps/#__tabbed_1_1
# pip install python-multipart
# pip install python-jose[cryptography] passlib[bcrypt]

from fastapi import Depends, FastAPI, Response, HTTPException, status
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn
import pandas as pd
from pydantic import BaseModel
# Sécurité des API
from typing import Annotated, Union, Optional
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
import random
import os

dossierTravail = "/ENTREPRISE_FILES/"
if not os.path.isdir(dossierTravail):
    os.makedirs(dossierTravail)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


# Création de l'application FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    oauth2_scheme
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/items")
async def read_users(token, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    return {"token": token}

# Connexion à la base de données MySQL via SQLAlchemy
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mypassword@studistatistiques_db_1:3306/ventes"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Définition du modèle de données
class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id = Column(Integer, primary_key=True, index=True)
    nom_utilisateur = Column(String(50), unique=True, index=True)
    nom = Column(String(50))
    prenom = Column(String(50))
    email = Column(String(50))
    mot_de_Passe = Column(String(50))

# Création de la table client
class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    classe_socio_professionnelle = Column(String(50), index=True)
    nb_enfants = Column(Integer)
    email = Column(String(50), unique=True, index=True)

# Collecte
class Collecte(Base):
    __tablename__ = "collecte"

    id = Column(Integer, primary_key=True, index=True)
    panier_client = Column(Float)
    date_passage = Column(Date)
    client_id = Column(Integer, ForeignKey('client.id'))

class DetailCollecte(Base):
    __tablename__ = "detail_collecte"

    id = Column(Integer, primary_key=True, index=True)
    collecte_id = Column(Integer, ForeignKey('collecte.id'))
    categorie_id = Column(Integer)
    montant = Column(Float)

class Categorie(Base):
    __tablename__ = "categorie"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String(50), index=True)

# Création de la table dans la base de données
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# la dépense du panier moyen en fonction de la catégorie socioprofessionnelle ;
average_basket_by_category = session.query(Client.classe_socio_professionnelle.label('label'), func.avg(Collecte.panier_client).label('montant_total')).join(Collecte).group_by(Client.classe_socio_professionnelle).all()

# la dépense du panier moyen en fonction de la catégorie socioprofessionnelle ;
# average_basket_by_csp = session.query(Client.classe_socio_professionnelle.label('label'), func.avg(Collecte.panier_client).label('montant_total')).join(Collecte).group_by(Client.classe_socio_professionnelle).all()

# les dépenses par catégorie en fonction de la catégorie socioprofessionnelle ;
depenses = session.query(Client.classe_socio_professionnelle, Categorie.libelle, func.sum(DetailCollecte.montant).label('montant_total'))
depenses = depenses.select_from(DetailCollecte)\
    .join(Collecte, Collecte.id == DetailCollecte.collecte_id)\
    .join(Client)\
    .join(Categorie, DetailCollecte.categorie_id == Categorie.id)
depenses = depenses.group_by(Client.classe_socio_professionnelle, Categorie.libelle)
total_spending_by_category = depenses.all()

# les dépenses par catégorie en fonction de la catégorie socioprofessionnelle ;
depensesParCsp = session.query(Client.classe_socio_professionnelle.label('label'), func.sum(DetailCollecte.montant).label('montant_total'))
depensesParCsp = depensesParCsp.select_from(DetailCollecte)\
    .join(Collecte, Collecte.id == DetailCollecte.collecte_id)\
    .join(Client)\
    .join(Categorie, DetailCollecte.categorie_id == Categorie.id)
depensesParCsp = depensesParCsp.group_by(Client.classe_socio_professionnelle)
total_depensesParCsp = depensesParCsp.all()

# les dépenses par catégorie en fonction de la catégorie socioprofessionnelle ;
depensesParCategorie = session.query(Categorie.libelle.label('label'), func.sum(DetailCollecte.montant).label('montant_total'))
depensesParCategorie = depensesParCategorie.select_from(DetailCollecte)\
    .join(Collecte, Collecte.id == DetailCollecte.collecte_id)\
    .join(Client)\
    .join(Categorie, DetailCollecte.categorie_id == Categorie.id)
depensesParCategorie = depensesParCategorie.group_by(Categorie.libelle)
total_depensesParCategorie = depensesParCategorie.all()

# donneesExport ;
donneesExport = session.query(Client.classe_socio_professionnelle, Categorie.libelle, DetailCollecte.montant)
donneesExport = donneesExport.select_from(DetailCollecte)\
    .join(Collecte, Collecte.id == DetailCollecte.collecte_id)\
    .join(Client)\
    .join(Categorie, DetailCollecte.categorie_id == Categorie.id)
# q = q.group_by(Client.classe_socio_professionnelle, Categorie.libelle)
donneesExport = donneesExport.all()
dataDonneesExport = pd.DataFrame(donneesExport)
donneesExportCsv = dataDonneesExport.to_csv(path_or_buf="/ENTREPRISE_FILES/donneesExportCsv.csv")

# donneesDetailCollecte ;
donneesDetailCollecte = session.query(DetailCollecte).all()

# for category, label, total_spending in total_spending_by_category:
#     print(f"{category} - {label}: {total_spending}")

# Route pour récupérer tous les utilisateurs
@app.get("/users")
async def read_users(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    users = db.query(Utilisateur).all()
    return users

@app.get("/depenses")
async def get_depenses(current_user: User = Depends(get_current_user)):
    # return total_spending_by_category
    rertour_total_spending_by_category = [row._asdict() for row in total_spending_by_category]
    return rertour_total_spending_by_category


@app.get("/depenses/categories")
async def get_depenses_categories(current_user: User = Depends(get_current_user)):
    rertour_total_depensesParCategorie = [row._asdict() for row in total_depensesParCategorie]
    return rertour_total_depensesParCategorie

@app.get("/depenses/csp")
async def get_depenses_csp(current_user: User = Depends(get_current_user)):
    # return total_depensesParCsp
    rertour_total_depensesParCsp = [row._asdict() for row in total_depensesParCsp]
    return rertour_total_depensesParCsp


@app.get("/paniermoyen/categories")
async def get_paniermoyen_categories(current_user: User = Depends(get_current_user)):
    # return average_basket_by_category
    rertour_average_basket_by_category = [row._asdict() for row in average_basket_by_category]
    return rertour_average_basket_by_category

# @app.get("/paniermoyen/csp")
# async def get_paniermoyen_csp(current_user: User = Depends(get_current_user)):
#     return average_basket_by_csp


@app.get("/export")
async def get_exportBrut(current_user: User = Depends(get_current_user)):
    rertour_donneesExport = [row._asdict() for row in donneesExport]
    return rertour_donneesExport

@app.get("/export_csv/{nbLignes}")
async def get_export_csv(nbLignes : int, current_user: User = Depends(get_current_user)):
    donneesExport = session.query(Client.classe_socio_professionnelle, Categorie.libelle, DetailCollecte.montant)
    donneesExport = donneesExport.select_from(DetailCollecte)\
    .join(Collecte, Collecte.id == DetailCollecte.collecte_id)\
    .join(Client)\
    .join(Categorie, DetailCollecte.categorie_id == Categorie.id)
    donneesExport = donneesExport.limit(nbLignes).all()
    dataDonneesExport = pd.DataFrame(donneesExport)
    donneesExportCsv = dataDonneesExport.to_csv(path_or_buf="/ENTREPRISE_FILES/donneesExportCsv.csv")

    return FileResponse("/ENTREPRISE_FILES/donneesExportCsv.csv", media_type='text/csv', filename='exported_data.csv')

@app.get("/donneesDetailCollecte")
async def get_donneesDetailCollecte():
    return donneesDetailCollecte

# TO DO : ajouter sécurité
# Route pour créer un utilisateur
@app.post("/users")
async def create_user(username: str, email: str):
    db = SessionLocal()
    user = Utilisateur(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/data/generate/{nbLignes}/{nbMaxCategories}")
async def generate_data(nbLignes : int, nbMaxCategories : int):
    # Générer 7 millions de lignes de données

    clients = session.query(Client).all()
    categories = session.query(Categorie).all()

    for i in range(nbLignes):
        panier_client = round(random.uniform(0.0, 100.0), 2)
        date_passage = datetime.today() - timedelta(days=random.randint(1, 365))
        client = session.query(Client).order_by(func.random()).first()
        collecte = Collecte(
            panier_client=panier_client,
            date_passage=date_passage,
            client_id=random.choice(clients).id
        )
        session.add(collecte)

        # Générer entre 1 et X (nbCategoriesDisponibles) lignes de detailCollecte
        nbCategoriesDisponibles = session.query(func.count(Categorie.id)).scalar()
        if nbCategoriesDisponibles < nbMaxCategories :
            nbMaxCategories = nbCategoriesDisponibles

        nombreCategoriesCollecte = random.randint(1, nbMaxCategories)
        categories = session.query(Categorie).limit(nombreCategoriesCollecte).all()
        nbcategoriesParcourues = 0
        total_montant = collecte.panier_client
        for categorie in categories:
            nbcategoriesParcourues = nbcategoriesParcourues+1
            if nbcategoriesParcourues == nombreCategoriesCollecte:
                # La dernière ligne de détail reçoit le reste du montant
                montant = total_montant
            else:
                # Répartir le montant restant sur les autres lignes de détail
                montant = random.uniform(0, total_montant)
                total_montant -= montant
            categorie_id=categorie.id

            detail_collecte = DetailCollecte(
                montant=montant,
                categorie_id=categorie_id,
                collecte_id=collecte.id
            )
            session.add(detail_collecte)

        # Enregistrer les données toutes les 10000 lignes
        if i % 1000 == 0:
            print("commit" + str(i))
            session.commit()
    session.commit()
    # Fermer la session
    session.close()
    return "ok"
    # VERIFIER :
        # (SELECT SUM(montant),0 FROM detail_collecte) UNION DISTINCT(SELECT 0, SUM(panier_client) FROM collecte); 
if __name__ =='__main__':
   uvicorn.run(app, host="127.0.0.1", port=8000)