from sqlalchemy.orm import Session
from app.models.models import Usuario, Analise
from app.models.schemas import UsuarioCreate
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str) -> str:
    """
    Gera hash da senha. Primeiro tenta o passlib; se falhar, usa bcrypt.hashpw direto.
    Retorna o hash como string.
    """
    if senha is None:
        raise ValueError("Senha não pode ser vazia")

    try:
        # tentativa preferencial: passlib (mantém compatibilidade com o resto do projeto)
        return pwd_context.hash(senha)
    except Exception as e:
        # fallback seguro: bcrypt puro
        try:
            hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
            return hashed.decode("utf-8")
        except Exception as e2:
            # log se tiver logger no projeto; aqui levantamos erro claro
            raise RuntimeError(f"Erro ao gerar hash da senha: {e} / {e2}")

def verificar_senha(senha_plana: str, senha_hashed: str) -> bool:
    """
    Verifica a senha. Tenta passlib primeiro, em seguida faz fallback para bcrypt.checkpw.
    """
    if not senha_hashed:
        return False

    try:
        return pwd_context.verify(senha_plana, senha_hashed)
    except UnknownHashError:
        # fallback para bcrypt (caso hash seja $2b$... e passlib não reconheça)
        try:
            return bcrypt.checkpw(senha_plana.encode("utf-8"), senha_hashed.encode("utf-8"))
        except Exception:
            return False
    except Exception:
        # qualquer outro erro -> não autentica
        return False


def criar_usuario(db: Session, usuario: UsuarioCreate):
    senha_hashed = hash_senha(usuario.senha)

    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hashed,  
        tipo_conta=usuario.tipo_conta
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def obter_usuario_por_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def obter_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def listar_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def deletar_usuario(db: Session, usuario_id: int):
    """
    Deleta um usuário pelo id. Remove antes as análises relacionadas para evitar
    erros de integridade quando a FK não aceita NULL.
    Retorna o objeto deletado ou None.
    """
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        return None

    # remover análises relacionadas diretamente no banco (evita UPDATE para NULL)
    db.query(Analise).filter(Analise.usuario_id == usuario_id).delete(synchronize_session=False)

    db.delete(db_usuario)
    db.commit()
    return db_usuario

def atualizar_usuario(db: Session, usuario_id: int, usuario_update):
    """
    Atualiza campos do usuário. usuario_update pode ser um Pydantic model com .dict(exclude_unset=True)
    ou um dict com os campos a atualizar. Se a senha for fornecida, será feita a hash.
    Retorna o usuário atualizado ou None se não existir.
    """
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        return None

    # obter dict com apenas campos enviados (caso seja Pydantic model)
    if hasattr(usuario_update, "dict"):
        data = usuario_update.dict(exclude_unset=True)
    elif isinstance(usuario_update, dict):
        data = {k: v for k, v in usuario_update.items() if v is not None}
    else:
        # objeto genérico: iterar atributos não-None
        data = {k: getattr(usuario_update, k) for k in ["nome", "email", "senha", "tipo_conta"] if getattr(usuario_update, k, None) is not None}

    if "senha" in data and data["senha"] is not None:
        data["senha"] = hash_senha(data["senha"])

    for key, value in data.items():
        setattr(db_usuario, key, value)

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
