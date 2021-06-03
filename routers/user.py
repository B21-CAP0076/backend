from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows
from fastapi.security.oauth2 import OAuth2
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from google.oauth2 import id_token
from google.auth.transport import requests

from config import settings
from db.mongodb import mongo_engine
from models.user import User, UserUpdate

# Packages needed for ML
from models.genre import Genre
from choice.education import EducationChoice
import sklearn.preprocessing as prep
import numpy as np
import tensorflow as tf
import joblib
import umap

router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.post("/gauth")
async def gauth(req: Request, engine: AIOEngine = Depends(mongo_engine)):
    try:
        id_info = id_token.verify_oauth2_token(req.query_params["token"], requests.Request(), settings.CLIENT_ID)
        user_id = id_info["sub"]

        user = await engine.find_one(User, User.gid == user_id)
        if user is None:
            name = id_info["name"]
            email = id_info["email"]
            picture = id_info["picture"]

            new_user = User(gid=user_id, name=name, email=email, picture=picture)
            await engine.save(new_user)

            return new_user

        # old user
        else:
            return user

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to validate Google login")


@router.put("/", response_model=User)
async def create(user: User, engine: AIOEngine = Depends(mongo_engine)):
    await engine.save(user)
    return user


@router.get("/")
async def get_all(
        page: int = 1,
        reading_cluster: Optional[int] = None,
        engine: AIOEngine = Depends(mongo_engine)
):
    skip: int = 50 * (page - 1)

    queries = []

    if reading_cluster:
        qe = QueryExpression({'reading_cluster': {'$eq': reading_cluster}})
        queries.append(qe)

    users = await engine.find(User, *queries, skip=skip, limit=50)
    return users


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    return user


@router.patch("/{id}", response_model=User)
async def update(id: ObjectId, patch: UserUpdate, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(user, name, value)
    await engine.save(user)
    return user


@router.delete("/{id}")
async def delete(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    await engine.delete(user)
    return user

@router.patch("/predict/{id}")
async def predict_user_cluser(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    # Preprocess user data section

    # Get user by Id
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    
    # Check user.age == isNotNull ? continue : raise error (age need to be filled first)
    if user.age is None:
        return {
            'isPredicted': False,
            'message': 'Data umur kosong. Silahkan isi umur terlebih dahulu.'
        }

    # Check user.education == isNotNull ? continue : raise error (education need to be filled first)
    if user.education is None:
        return {
            'isPredicted': False,
            'message': 'Data pendidikan kosong. Silahkan isi pendidikan terlebih dahulu.'
        }

    # Check user.genre_preferences == isNotNull ? continue : raise error (genre preference need to be filled first)
    if user.genre_preferences is None:
        return {
            'isPredicted': False,
            'message': 'Data preferensi genre buku kosong. Silahkan isi preferensi genre buku terlebih dahulu.'
        }

    # Change age to np array
    user_age = np.array([[user.age]])

    # One hot encode user.education using list education as encoder categories
    user_edu_encoded = encode_education(user.education)
    
    # One hot encode user.genre_preferences using list genre as encoder categories
    genre_list = await engine.find(Genre)
    user_genre_encoded = encode_genre(user.genre_preferences, genre_list)
    
    # Predict user cluster section
    # Pass Data to TF AutoEncoder Model
    combined_user_data_np = np.concatenate((user_age[0], user_edu_encoded[0], user_genre_encoded[0]))
    combined_user_data_tensor = tf.convert_to_tensor([combined_user_data_np])

    ae_model = tf.keras.models.load_model('ml-assets/habitech_autoencoder')
    ae_result = ae_model.predict(combined_user_data_tensor)

    # Pass embedded data to UMAP
    # Currently, by load saved umap model will create error (Incompatible bytecode version)
    # umap_model = joblib.load('ml-assets/habitech_umap.sav')
    umap_model = umap.UMAP(n_neighbors=20, n_components=33, metric='euclidean', min_dist=0, random_state=0)
    umap_result = umap_model.fit_transform(ae_result)

    # Pass Data that has been processed by UMAP to GMM
    gmm_model = joblib.load('ml-assets/habitech_gmm.sav')
    gmm_result = gmm_model.predict_proba(umap_result)

    # Get cluster
    cluster_predicted = gmm_result.argmax(1)

    # Update user.reading_cluster
    setattr(user, 'reading_cluster', cluster_predicted[0])
    await engine.save(user)

    return {
        'isPredicted': True,
        'userData': user
    }

def encode_education(user_edu):
    edu_list = [edu.value for edu in EducationChoice]

    enc_edu = prep.OneHotEncoder(categories=[edu_list])

    # Need to be in 2D Array (currently in String)
    enc_edu_fit = enc_edu.fit_transform([[user_edu]])

    return enc_edu_fit.toarray()

def encode_genre(user_genre_pref, genre_list_db):
    user_genre_pref = [user_genre.name for user_genre in user_genre_pref]
    genre_list = [genre.name for genre in genre_list_db]
    
    # Encode genre one by one
    encoded_genre_pref = []
    for genre in user_genre_pref:
        enc_genre = prep.OneHotEncoder(categories=[genre_list])

        # Need to be in 2D Array (currently in String)
        enc_genre_fit = enc_genre.fit_transform([[genre]])
        encoded_genre_pref.append(enc_genre_fit.toarray())
    
    # Combine all encoded genre
    combined_genre = encoded_genre_pref[0]
    for encoded_genre in encoded_genre_pref[1:]:
        combined_genre = np.add(combined_genre, encoded_genre)

    return combined_genre