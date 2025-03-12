"""Creación de user y password model

Revision ID: 0f069245f555
Revises: 778081c328a9
Create Date: 2025-03-11 10:55:00.025450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f069245f555'
down_revision = '778081c328a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('primer_nombre', sa.String(length=50), nullable=False),
    sa.Column('segundo_nombre', sa.String(length=50), nullable=True),
    sa.Column('apellido_paterno', sa.String(length=50), nullable=False),
    sa.Column('apellido_materno', sa.String(length=50), nullable=False),
    sa.Column('correo', sa.String(length=100), nullable=False),
    sa.Column('telefono', sa.String(length=20), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('fecha_actualizacion', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo')
    )
    op.create_table('passwords',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['id_usuario'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('passwords')
    op.drop_table('users')
    # ### end Alembic commands ###
