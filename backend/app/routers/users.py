# ============================================================
# routers/users.py — Endpoints de la API para gestión de usuarios
# ============================================================
# Un "endpoint" es una URL que tu app puede llamar.
# Este router gestiona todo lo relacionado con /users
#
# Lo que tendrás disponible:
#   GET    /users/          → Lista todos los usuarios
#   GET    /users/{id}      → Obtiene un usuario por su ID
#   POST   /users/          → Crea un nuevo usuario
#   PATCH  /users/{id}      → Actualiza campos de un usuario
#   DELETE /users/{id}      → Elimina un usuario
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db           # La función que abre/cierra sesiones con la BD
from app.models.user import User          # El modelo (tabla) de usuario
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)

# Creamos el router — es como un "mini-FastAPI" que luego conectaremos al principal
router = APIRouter()


# ────────────────────────────────────────────────────────────
# GET /users/  →  Listar todos los usuarios
# ────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=List[UserResponse],      # Devuelve una lista de usuarios
    summary="Listar todos los usuarios",
)
def get_users(
    skip: int = 0,       # Página: empieza desde el usuario N
    limit: int = 100,    # Máximo de usuarios por página
    db: Session = Depends(get_db),
):
    """
    Devuelve todos los usuarios de la base de datos.
    - **skip**: cuántos registros saltar (para paginación)
    - **limit**: máximo de registros a devolver
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# ────────────────────────────────────────────────────────────
# GET /users/{user_id}  →  Obtener un usuario por ID
# ────────────────────────────────────────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener un usuario por ID",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Busca un usuario por su ID.
    Si no existe, devuelve un error 404.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    return user


# ────────────────────────────────────────────────────────────
# POST /users/  →  Crear un nuevo usuario
# ────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,    # 201 = "Creado con éxito"
    summary="Crear un nuevo usuario",
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    El email y el username deben ser únicos.
    """
    # Comprobamos si ya existe un usuario con ese email
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese email",
        )

    # Comprobamos si ya existe un usuario con ese username
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ese username ya está en uso",
        )

    # Creamos el objeto User con los datos recibidos
    new_user = User(**user_data.model_dump())

    db.add(new_user)        # Añade el usuario a la sesión (todavía no se guarda)
    db.commit()             # Guarda definitivamente en la base de datos
    db.refresh(new_user)    # Recarga para obtener el id y created_at asignados por la BD

    return new_user


# ────────────────────────────────────────────────────────────
# PATCH /users/{user_id}  →  Actualizar un usuario
# ────────────────────────────────────────────────────────────
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar datos de un usuario",
)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los campos de un usuario.
    Solo tienes que enviar los campos que quieres cambiar.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )

    # model_dump(exclude_unset=True) devuelve solo los campos que se enviaron
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)   # Actualiza cada campo del objeto

    db.commit()
    db.refresh(user)
    return user


# ────────────────────────────────────────────────────────────
# DELETE /users/{user_id}  →  Eliminar un usuario
# ────────────────────────────────────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,  # 204 = "Borrado, sin contenido que devolver"
    summary="Eliminar un usuario",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos permanentemente.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )

    db.delete(user)
    db.commit()
    # No devolvemos nada (204 No Content)
