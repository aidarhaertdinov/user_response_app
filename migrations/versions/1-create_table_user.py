"""empty message

Revision ID: 1-create_table_user
Revises: 
Create Date: 2023-03-12 00:24:01.719139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1-create_table_user'
down_revision = None
branch_labels = None
depends_on = None

from werkzeug.security import generate_password_hash
from datetime import datetime
from app import moment


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    user_table = op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=70), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('permission', sa.Enum('MODERATE', 'ADMIN', 'USER', name='permissions'), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###

    op.bulk_insert(user_table,
                   [
                       {'email': 'admin@mail.ru',
                        'username': 'Aдминистратор',
                        'permission': 'ADMIN',
                        'created_date': moment.create(datetime.utcnow()).timestamp,
                        'password_hash': generate_password_hash(password='admin123')},
                       {'email': 'swagger@mail.ru',
                        'username': 'swagger_user',
                        'permission': 'USER',
                        'created_date': moment.create(datetime.utcnow()).timestamp,
                        'password_hash': generate_password_hash(password='swagger123')}
                   ]
                   )

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
