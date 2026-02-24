from app.database import engine
from sqlalchemy import text

def run_migrations():
    with engine.connect() as conn:
        migrations = [
            # Users table
            ("users", "is_active", "ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1"),
            
            # Companies table
            ("companies", "industry", "ALTER TABLE companies ADD COLUMN industry VARCHAR"),
            ("companies", "location", "ALTER TABLE companies ADD COLUMN location VARCHAR"),
            
            # Jobs table
            ("jobs", "updated_date", "ALTER TABLE jobs ADD COLUMN updated_date DATETIME"),
            ("jobs", "is_active", "ALTER TABLE jobs ADD COLUMN is_active BOOLEAN DEFAULT 1"),
            
            # Resumes table
            ("resumes", "file_path", "ALTER TABLE resumes ADD COLUMN file_path VARCHAR"),
            ("resumes", "processed_text", "ALTER TABLE resumes ADD COLUMN processed_text TEXT"),
            ("resumes", "keywords", "ALTER TABLE resumes ADD COLUMN keywords TEXT DEFAULT '[]'"),
        ]

        for table, col, sql in migrations:
            try:
                conn.execute(text(sql))
                print(f"Added {col} to {table}")
            except Exception:
                print(f"  skip: {table}.{col} already exists")

        # Fix NULL values
        updates = [
            "UPDATE users SET is_active = 1 WHERE is_active IS NULL",
            "UPDATE jobs SET is_active = 1 WHERE is_active IS NULL",
            "UPDATE resumes SET keywords = '[]' WHERE keywords IS NULL",
            "UPDATE resumes SET processed_text = raw_text WHERE processed_text IS NULL",
        ]

        for sql in updates:
            try:
                conn.execute(text(sql))
                print(f"Updated defaults")
            except Exception as e:
                print(f"  skip: {e}")

        conn.commit()
        print()
        print("ALL MIGRATIONS COMPLETE!")

def verify_tables():
    tables = ["users", "companies", "jobs", "resumes", "applications", "job_matches"]
    with engine.connect() as conn:
        print("=== TABLE COLUMNS ===")
        for table in tables:
            try:
                result = conn.execute(text(f"PRAGMA table_info({table})"))
                cols = [row[1] for row in result]
                print(f"{table}: {cols}")
            except Exception as e:
                print(f"{table}: ERROR - {e}")

def verify_data():
    from app.database import SessionLocal
    from app.models import Company, Job, User, Application
    db = SessionLocal()
    print()
    print("=== DATA COUNT ===")
    print(f"Companies: {db.query(Company).count()}")
    print(f"Jobs: {db.query(Job).count()}")
    print(f"Users: {db.query(User).count()}")
    print(f"Applications: {db.query(Application).count()}")
    db.close()

if __name__ == "__main__":
    run_migrations()
    verify_tables()
    verify_data()