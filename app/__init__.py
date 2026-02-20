from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import threading
import time
import os
import logging

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        from app import routes, models
        db.create_all()
        from app.models import User
        from werkzeug.security import generate_password_hash
        from config import Config

        # Schema Migration for User Preferences - More robust timeout handling
        try:
            from sqlalchemy import text
            
            # Always rollback any existing transaction first
            try:
                db.session.rollback()
            except Exception:
                pass
            
            # Set unlimited timeout to prevent statement cancellation
            try:
                db.session.execute(text("SET LOCAL statement_timeout = 0"))
                db.session.commit()
                print("✅ Database timeout disabled for migrations")
            except Exception:
                pass  # Continue even if we can't set timeout
            
            # Check database dialect and handle accordingly
            try:
                eng = db.session.get_bind()
                print(f"✅ Database engine binding successful: {eng.dialect.name}")
            except Exception as bind_error:
                print(f"⚠️ Database engine binding failed: {bind_error}")
                # Continue with basic operations
            
            # Check if columns exist
            if 'sqlite' in eng.dialect.name if 'eng' in locals() else False:
                 res = db.session.execute(text("PRAGMA table_info(users)")).fetchall()
                 cols = [r[1] for r in res]
                 if 'pref_course' not in cols:
                     db.session.execute(text("ALTER TABLE users ADD COLUMN pref_course TEXT"))
                 if 'pref_semester' not in cols:
                     db.session.execute(text("ALTER TABLE users ADD COLUMN pref_semester TEXT"))
                 if 'pref_subject' not in cols:
                     db.session.execute(text("ALTER TABLE users ADD COLUMN pref_subject TEXT"))
                 db.session.commit()
            else:
                 # Postgres - more robust approach
                 try:
                     db.session.execute(text("ALTER TABLE public.users ADD COLUMN IF NOT EXISTS pref_course VARCHAR(100)"))
                     db.session.execute(text("ALTER TABLE public.users ADD COLUMN IF NOT EXISTS pref_semester VARCHAR(20)"))
                     db.session.execute(text("ALTER TABLE public.users ADD COLUMN IF NOT EXISTS pref_subject VARCHAR(100)"))
                     db.session.commit()
                     print("✅ PostgreSQL user preference columns ensured")
                 except Exception as ex:
                     db.session.rollback()
                     print(f"⚠️ User columns migration note: {ex}")
                     # Continue anyway - not critical

        except Exception as e:
            db.session.rollback()
            print(f"Initial migration setup failed: {e}")

        except Exception as e:
            db.session.rollback()
            print(f"Initial migration setup failed: {e}")

        admin = User.query.filter_by(email=Config.ADMIN_EMAIL).first()
        if not admin:
            db.session.add(User(email=Config.ADMIN_EMAIL, password_hash=generate_password_hash(Config.ADMIN_PASSWORD), role='admin'))
            db.session.commit()
        
        # Register Blueprints
        print("🔄 Registering blueprints...")
        app.register_blueprint(routes.bp)
        print("✅ Blueprints registered")
        
        # Automatic index rebuild on startup with persistent storage
        print("🔄 Initializing vector store...")
        from app.services.vector_store import VectorStore
        from app.models import DocumentChunk
        from app.services.ai_service import AIService
        from app.routes import sync_storage
        from app.services.index_rebuilder import rebuild_index_from_db  # Import the new rebuilder
        
        # Initialize vector store with Supabase persistent storage
        print("🔄 Getting vector store instance...")
        vector_store = VectorStore.get_instance()  # Use singleton instance
        print("✅ Vector store instance ready")
        index_name = 'vector_index'
        
        # Check if we need to rebuild (only if index is empty)
        print("🔄 Checking vector store stats...")
        current_stats = vector_store.get_stats()
        print(f"📊 Current stats: {current_stats}")
        if current_stats['total_vectors'] == 0:
            # Rebuild index from database on startup (this handles Render's ephemeral filesystem)
            print("🔄 Starting vector index rebuild from database...")
            logging.info("🔄 Starting vector index rebuild from database...")
            try:
                # First try to load existing index from Supabase storage
                from app.services.vector_store import VectorStore
                vector_store = VectorStore.get_instance()
                # Skip loading from Supabase since we're rebuilding in-memory on each startup for Render compatibility
                print("🔄 Rebuilding vector index from database for Render compatibility...")
                logging.info("Rebuilding vector index from database for Render compatibility...")
                print("🔄 Calling rebuild_index_from_db...")
                rebuild_index_from_db()
                print("✅ rebuild_index_from_db completed")
                
                # Final validation
                final_stats = vector_store.get_stats()
                print(f"📊 Final vector store stats: {final_stats}")
                logging.info(f"📊 Final vector store stats: {final_stats}")
                
                # Log for debugging purposes
                if final_stats['total_vectors'] == 0:
                    print("❌ CRITICAL: Vector store has 0 vectors after rebuild - chat will not work!")
                    logging.critical("CRITICAL: Vector store has 0 vectors after rebuild - chat will not work!")
                else:
                    print(f"✅ Vector store is ready with {final_stats['total_vectors']} vectors")
                    logging.info(f"✅ Vector store is ready with {final_stats['total_vectors']} vectors")
                    
            except Exception as e:
                print(f"❌ Vector index rebuild failed: {e}")
                logging.error(f"❌ Vector index rebuild failed: {e}", exc_info=True)
                # Continue anyway - the vector store will be empty but the app should still start
        else:
            print(f"✅ Vector store already has {current_stats['total_vectors']} vectors, skipping rebuild")
            logging.info(f"✅ Vector store already has {current_stats['total_vectors']} vectors, skipping rebuild")
        
        # Start background workers (Web Source Auto-Refresh) - delayed start to not block app startup
        try:
            from app.services.web_source_refresher import WebSourceRefresher
            # Start with longer initial delay to let main app initialize
            import threading
            import time
            
            def delayed_worker_start():
                time.sleep(10)  # Wait 10 seconds for app to fully start
                try:
                    WebSourceRefresher.start_worker(app)
                    print("🚀 Web Source Auto-Refresher started.")
                    logging.info("Web Source Auto-Refresher started.")
                except Exception as e:
                    print(f"❌ Failed to start WebSourceRefresher: {e}")
                    logging.error(f"❌ Failed to start WebSourceRefresher: {e}")
            
            # Start in background thread
            worker_thread = threading.Thread(target=delayed_worker_start, daemon=True)
            worker_thread.start()
            print("⏰ Web Source Auto-Refresher scheduled to start in 10 seconds...")
            logging.info("Web Source Auto-Refresher scheduled to start in 10 seconds...")
            
        except Exception as e:
            print(f"❌ Failed to schedule WebSourceRefresher: {e}")
            logging.error(f"❌ Failed to schedule WebSourceRefresher: {e}")

    return app