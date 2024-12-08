"""remove_album_publisher_and_add_constraints

Revision ID: 001
Revises: 
Create Date: 2024-01-10

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Drop album_publisher column from stickers table
    op.drop_column('stickers', 'album_publisher')
    
    # Drop album_publisher column from packs table
    op.drop_column('packs', 'album_publisher')
    
    # Drop album_publisher column from boxes table
    op.drop_column('boxes', 'album_publisher')
    
    # Add check constraints
    op.create_check_constraint(
        'check_rarity_level',
        'stickers',
        'sticker_rarity_level BETWEEN 1 AND 5'
    )
    
    op.create_check_constraint(
        'check_sticker_count',
        'packs',
        'pack_sticker_count > 0'
    )
    
    op.create_check_constraint(
        'check_pack_quantity',
        'collector_packs',
        'collector_pack_quantity > 0'
    )
    
    op.create_check_constraint(
        'check_pack_count',
        'boxes',
        'box_pack_count > 0'
    )
    
    op.create_check_constraint(
        'check_box_quantity',
        'collector_boxes',
        'collector_box_quantity > 0'
    )

def downgrade() -> None:
    # Remove check constraints
    op.drop_constraint('check_rarity_level', 'stickers')
    op.drop_constraint('check_sticker_count', 'packs')
    op.drop_constraint('check_pack_quantity', 'collector_packs')
    op.drop_constraint('check_pack_count', 'boxes')
    op.drop_constraint('check_box_quantity', 'collector_boxes')
    
    # Add back album_publisher columns
    op.add_column('stickers', sa.Column('album_publisher', sa.Integer, sa.ForeignKey('albums.id')))
    op.add_column('packs', sa.Column('album_publisher', sa.Integer, sa.ForeignKey('albums.id')))
    op.add_column('boxes', sa.Column('album_publisher', sa.Integer, sa.ForeignKey('albums.id')))
