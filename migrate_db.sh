docker exec opensponsor_app python -c '
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    cols = [r[1] for r in conn.execute(text("PRAGMA table_info(ads);")).fetchall()]
    print("CURRENT COLS:", cols)
    if "target_repo_id" not in cols:
        conn.execute(text("ALTER TABLE ads ADD COLUMN target_repo_id INTEGER;"))
        conn.commit()
        print("ADDED target_repo_id TO ads TABLE SUCCESSFULLY!")
    else:
        print("target_repo_id ALREADY EXISTS")
'
