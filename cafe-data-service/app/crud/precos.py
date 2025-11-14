from sqlalchemy.orm import Session
from datetime import date  # ADICIONE ESTA LINHA
from app.models.models import ArabicaPrice, RobustaPrice
from app.models.schemas import ArabicaPriceCreate, RobustaPriceCreate, ArabicaPriceUpdate, RobustaPriceUpdate

# Operações para Arabica
def criar_arabica_price(db: Session, arabica_price: ArabicaPriceCreate):
    db_arabica_price = ArabicaPrice(
        price_date=arabica_price.price_date,
        price=arabica_price.price
    )
    db.add(db_arabica_price)
    db.commit()
    db.refresh(db_arabica_price)
    return db_arabica_price

def obter_arabica_price_por_id(db: Session, arabica_price_id: int):
    return db.query(ArabicaPrice).filter(ArabicaPrice.id == arabica_price_id).first()

def obter_arabica_price_por_data(db: Session, price_date: date):
    return db.query(ArabicaPrice).filter(ArabicaPrice.price_date == price_date).first()

def listar_arabica_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ArabicaPrice).order_by(ArabicaPrice.price_date.desc()).offset(skip).limit(limit).all()

# def atualizar_arabica_price(db: Session, arabica_price_id: int, arabica_price_update: ArabicaPriceUpdate):
#     db_arabica_price = db.query(ArabicaPrice).filter(ArabicaPrice.id == arabica_price_id).first()
#     if db_arabica_price:
#         update_data = arabica_price_update.dict(exclude_unset=True)
#         for key, value in update_data.items():
#             setattr(db_arabica_price, key, value)
#         db.commit()
#         db.refresh(db_arabica_price)
#     return db_arabica_price

def deletar_arabica_price(db: Session, arabica_price_id: int):
    db_arabica_price = db.query(ArabicaPrice).filter(ArabicaPrice.id == arabica_price_id).first()
    if db_arabica_price:
        db.delete(db_arabica_price)
        db.commit()
    return db_arabica_price

# Operações para Robusta
def criar_robusta_price(db: Session, robusta_price: RobustaPriceCreate):
    db_robusta_price = RobustaPrice(
        price_date=robusta_price.price_date,
        price=robusta_price.price
    )
    db.add(db_robusta_price)
    db.commit()
    db.refresh(db_robusta_price)
    return db_robusta_price

def obter_robusta_price_por_id(db: Session, robusta_price_id: int):
    return db.query(RobustaPrice).filter(RobustaPrice.id == robusta_price_id).first()

def obter_robusta_price_por_data(db: Session, price_date: date):
    return db.query(RobustaPrice).filter(RobustaPrice.price_date == price_date).first()

def listar_robusta_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RobustaPrice).order_by(RobustaPrice.price_date.desc()).offset(skip).limit(limit).all()

# def atualizar_robusta_price(db: Session, robusta_price_id: int, robusta_price_update: RobustaPriceUpdate):
#     db_robusta_price = db.query(RobustaPrice).filter(RobustaPrice.id == robusta_price_id).first()
#     if db_robusta_price:
#         update_data = robusta_price_update.dict(exclude_unset=True)
#         for key, value in update_data.items():
#             setattr(db_robusta_price, key, value)
#         db.commit()
#         db.refresh(db_robusta_price)
#     return db_robusta_price

def deletar_robusta_price(db: Session, robusta_price_id: int):
    db_robusta_price = db.query(RobustaPrice).filter(RobustaPrice.id == robusta_price_id).first()
    if db_robusta_price:
        db.delete(db_robusta_price)
        db.commit()
    return db_robusta_price

# Operações para obter preços mais recentes
def obter_ultimo_preco_arabica(db: Session):
    return db.query(ArabicaPrice).order_by(ArabicaPrice.price_date.desc()).first()

def obter_ultimo_preco_robusta(db: Session):
    return db.query(RobustaPrice).order_by(RobustaPrice.price_date.desc()).first()

# Operações para deletar preço mais antigo
def deletar_preco_mais_antigo_arabica(db: Session):
    preco_antigo = db.query(ArabicaPrice).order_by(ArabicaPrice.price_date.asc()).first()
    if preco_antigo:
        db.delete(preco_antigo)
        db.commit()
        return preco_antigo
    return None

def deletar_preco_mais_antigo_robusta(db: Session):
    preco_antigo = db.query(RobustaPrice).order_by(RobustaPrice.price_date.asc()).first()
    if preco_antigo:
        db.delete(preco_antigo)
        db.commit()
        return preco_antigo
    return None