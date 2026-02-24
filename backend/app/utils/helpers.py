# # claude

# import json

# from datetime import datetime
# from ..database import SessionLocal
# from ..models import Job, Company
# from ..auth import get_password_hash

# def seed_jobs():
#     """Seed database with sample jobs"""
#     db = SessionLocal()
    
#     # Check if jobs already exist
#     existing_jobs = db.query(Job).count()
#     if existing_jobs > 0:
#         print(f"Database already has {existing_jobs} jobs. Skipping seed.")
#         return
    
#     try:
#         with open('data/sample_jobs.json', 'r') as f:
#             jobs_data = json.load(f)
        
#         for job_data in jobs_data:
#             job = Job(**job_data)
#             db.add(job)
        
#         db.commit()
#         print(f"Successfully seeded {len(jobs_data)} jobs!")
        
#     except Exception as e:
#         print(f"Error seeding jobs: {str(e)}")
#         db.rollback()
#     finally:
#         db.close()

# def seed_companies():
#     """Seed database with sample companies"""
#     db = SessionLocal()
    
#     # Check if companies already exist
#     existing_companies = db.query(Company).count()
#     if existing_companies > 0:
#         print(f"Database already has {existing_companies} companies. Skipping seed.")
#         return
    
#     try:
#         with open('data/sample_jobs.json', 'r') as f:
#             jobs_data = json.load(f)
        
#         companies_created = set()
        
#         for job in jobs_data:
#             company_name = job.get('company')
#             company_email = job.get('company_email', f"hr@{company_name.lower().replace(' ', '')}.com")
            
#             if company_name not in companies_created:
#                 company = Company(
#                     name=company_name,
#                     email=company_email,
#                     hashed_password=get_password_hash("password123"),  # Default password
#                     description=f"Leading company in the industry"
#                 )
#                 db.add(company)
#                 companies_created.add(company_name)
        
#         db.commit()
#         print(f"Successfully seeded {len(companies_created)} companies!")
#         print("Default password for all HRs: password123")
        
#     except Exception as e:
#         print(f"Error seeding companies: {str(e)}")
#         db.rollback()
#     finally:
#         db.close()

# if __name__ == "__main__":
#     seed_jobs()
#     seed_companies()




# import json
# from ..database import SessionLocal
# from ..models import Job, Company
# from ..auth import get_password_hash


# DATA_FILE = "data/sample_jobs.json"


# def seed_companies():
#     """Seed companies from sample_jobs.json"""
#     db = SessionLocal()

#     try:
#         if db.query(Company).count() > 0:
#             print("Companies already exist. Skipping company seeding.")
#             return

#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             jobs_data = json.load(f)

#         created = {}

#         for job in jobs_data:
#             name = job["company"]
#             email = job.get("company_email")

#             if name not in created:
#                 company = Company(
#                     name=name,
#                     email=email,
#                     hashed_password=get_password_hash("password123"),
#                     description=f"HR account for {name}",
#                     website=None,
#                     is_hr=True,
#                 )
#                 db.add(company)
#                 db.commit()
#                 db.refresh(company)

#                 created[name] = company

#         print(f"Seeded {len(created)} companies.")
#         print("Default HR password: password123")

#     except Exception as e:
#         db.rollback()
#         print("Error seeding companies:", e)
#     finally:
#         db.close()


# def seed_jobs():
#     """Seed jobs from sample_jobs.json"""
#     db = SessionLocal()

#     try:
#         if db.query(Job).count() > 0:
#             print("Jobs already exist. Skipping job seeding.")
#             return

#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             jobs_data = json.load(f)

#         for job_data in jobs_data:
#             company = db.query(Company).filter_by(
#                 email=job_data["company_email"]
#             ).first()

#             if not company:
#                 print(f"Skipping job, company not found: {job_data['company']}")
#                 continue

#             job = Job(
#                 title=job_data["title"],
#                 location=job_data.get("location"),
#                 description=job_data["description"],
#                 requirements=job_data.get("requirements"),
#                 salary_range=job_data.get("salary_range"),
#                 job_type=job_data.get("job_type"),
#                 company_id=company.id,
#                 company_name=company.name,
#             )

#             db.add(job)

#         db.commit()
#         print(f"Seeded {len(jobs_data)} jobs successfully.")

#     except Exception as e:
#         db.rollback()
#         print("Error seeding jobs:", e)
#     finally:
#         db.close()


# def seed_all():
#     seed_companies()
#     seed_jobs()


# if __name__ == "__main__":
#     seed_all()


#working





# import json
# from datetime import datetime
# from ..database import SessionLocal
# from ..models import Job, Company
# from ..auth import get_password_hash

# DATA_FILE = "data/sample_jobs.json"

# def seed_companies():
#     """Seed companies from sample_jobs.json"""
#     db = SessionLocal()

#     try:
#         if db.query(Company).count() > 0:
#             print("Companies already exist. Skipping company seeding.")
#             return

#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             jobs_data = json.load(f)

#         created = {}

#         for job in jobs_data:
#             name = job["company"]
#             email = job.get("company_email")

#             if name not in created and email:
#                 company = Company(
#                     name=name,
#                     email=email,
#                     hashed_password=get_password_hash("password123"),
#                     description=f"Leading company in {name}",
#                     website=None,
#                     is_hr=True,
#                 )
#                 db.add(company)
#                 created[name] = True

#         db.commit()
#         print(f"✓ Seeded {len(created)} companies successfully!")
#         print("✓ Default HR password: password123")

#     except Exception as e:
#         db.rollback()
#         print(f"✗ Error seeding companies: {e}")
#     finally:
#         db.close()


# def seed_jobs():
#     """Seed jobs from sample_jobs.json"""
#     db = SessionLocal()

#     try:
#         existing_jobs = db.query(Job).count()
#         if existing_jobs > 0:
#             print(f"Jobs already exist ({existing_jobs} jobs). Skipping job seeding.")
#             return

#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             jobs_data = json.load(f)

#         jobs_created = 0
        
#         for job_data in jobs_data:
#             # Find company by email
#             company_email = job_data.get("company_email")
#             company = None
            
#             if company_email:
#                 company = db.query(Company).filter(Company.email == company_email).first()
            
#             # If company not found, try by name
#             if not company:
#                 company_name = job_data.get("company")
#                 company = db.query(Company).filter(Company.name == company_name).first()

#             # Create job
#             job = Job(
#                 title=job_data["title"],
#                 company=job_data["company"],  # This is the string field
#                 company_id=company.id if company else None,  # This is the foreign key
#                 location=job_data.get("location"),
#                 description=job_data["description"],
#                 requirements=job_data.get("requirements"),
#                 salary_range=job_data.get("salary_range"),
#                 job_type=job_data.get("job_type", "Full-time"),
#                 posted_date=datetime.utcnow()
#             )

#             db.add(job)
#             jobs_created += 1

#         db.commit()
#         print(f"✓ Seeded {jobs_created} jobs successfully!")

#     except Exception as e:
#         db.rollback()
#         print(f"✗ Error seeding jobs: {e}")
#         import traceback
#         traceback.print_exc()
#     finally:
#         db.close()


# def seed_all():
#     """Seed both companies and jobs"""
#     print("Starting database seeding...")
#     seed_companies()
#     seed_jobs()
#     print("Seeding complete!")


# if __name__ == "__main__":
#     seed_all()





import json
from datetime import datetime
from ..database import SessionLocal
from ..models import Job, Company
from ..auth import get_password_hash

DATA_FILE = "data/sample_jobs.json"


def seed_companies():
    """Seed companies - each gets a unique bcrypt-hashed password"""
    db = SessionLocal()
    try:
        if db.query(Company).count() > 0:
            print("Companies already exist. Skipping.")
            return

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)

        created = {}
        for job in jobs_data:
            name = job["company"]
            email = job.get("company_email", f"hr@{name.lower().replace(' ', '')}.com")

            if name not in created:
                # Each company gets unique password derived from their name
                # HR must change this after first login
                raw_password = f"{name.replace(' ', '').lower()}@2024"
                company = Company(
                    name=name,
                    email=email,
                    hashed_password=get_password_hash(raw_password),
                    description=f"HR account for {name}",
                    is_hr=True,
                )
                db.add(company)
                created[name] = {"email": email, "password": raw_password}

        db.commit()
        print(f"✓ Seeded {len(created)} companies")
        print("\n=== COMPANY LOGIN CREDENTIALS ===")
        for name, creds in created.items():
            print(f"  {name}: {creds['email']} / {creds['password']}")

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def seed_jobs():
    """Seed jobs and link them to companies"""
    db = SessionLocal()
    try:
        if db.query(Job).count() > 0:
            print("Jobs already exist. Skipping.")
            return

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)

        count = 0
        for job_data in jobs_data:
            company_email = job_data.get("company_email")
            company = None

            if company_email:
                company = db.query(Company).filter(Company.email == company_email).first()
            if not company:
                company = db.query(Company).filter(Company.name == job_data["company"]).first()

            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                company_id=company.id if company else None,
                location=job_data.get("location"),
                description=job_data["description"],
                requirements=job_data.get("requirements"),
                salary_range=job_data.get("salary_range"),
                job_type=job_data.get("job_type", "Full-time"),
                is_active=True,
                posted_date=datetime.utcnow()
            )
            db.add(job)
            count += 1

        db.commit()
        print(f"✓ Seeded {count} jobs")

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def seed_all():
    seed_companies()
    seed_jobs()