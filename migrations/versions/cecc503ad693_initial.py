"""Initial

Revision ID: cecc503ad693
Revises: 
Create Date: 2020-08-08 17:21:24.590399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cecc503ad693'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('directories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=False),
    sa.Column('removed', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['directories.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_index(op.f('ix_directories_created_at'), 'directories', ['created_at'], unique=False)
    op.create_table('file_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('removed', sa.Boolean(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['directories.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['file_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_files_created_at'), 'files', ['created_at'], unique=False)
    op.create_index(op.f('ix_files_updated_at'), 'files', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_files_updated_at'), table_name='files')
    op.drop_index(op.f('ix_files_created_at'), table_name='files')
    op.drop_table('files')
    op.drop_table('file_types')
    op.drop_index(op.f('ix_directories_created_at'), table_name='directories')
    op.drop_table('directories')
    # ### end Alembic commands ###