import sqlite3

from fastapi import APIRouter, HTTPException, status

from auth import create_access_token, get_password_hash, verify_password
from database import get_connection
from schemas import TokenResponse, UserCreate, UserLogin, UserResponse


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def register_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (email, password_hash)
                VALUES (?, ?)
                """,
                (user.email, hashed_password),
            )

            row = connection.execute(
                """
                SELECT id, email, created_at
                FROM users
                WHERE id = ?
                """,
                (cursor.lastrowid,),
            ).fetchone()

            return dict(row)

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado.",
        )


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin):
    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (credentials.email,),
        ).fetchone()

    if user is None or not verify_password(
        credentials.password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user["id"])

    return {
        "access_token": token,
        "token_type": "bearer",
    }
