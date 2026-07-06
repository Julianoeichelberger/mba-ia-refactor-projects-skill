import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
DB_PATH = os.environ.get('DB_PATH', 'loja.db')
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')

VALID_CATEGORIES = ['informatica', 'moveis', 'vestuario', 'geral', 'eletronicos', 'livros']
VALID_ORDER_STATUSES = ['pendente', 'aprovado', 'enviado', 'entregue', 'cancelado']

DISCOUNT_TIERS = [
    (10000, 0.10),
    (5000, 0.05),
    (1000, 0.02),
]
