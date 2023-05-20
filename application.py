"""
<!-- -| 
  * Weggo is a registered trademark in Spain as Plataforma Weggo España, S.L
  * Any disclosure of this code violates intellectual property laws.
  * Developed by Ruben Ayuso. 
|- -->
"""

from app import weggo_app
application = weggo_app()

if __name__ == "__main__":
  from config.config import application_env
  if application_env == 'development':
    application.run(port=5000)
  else:
    from waitress import serve
    serve(application, host="0.0.0.0", port=8080)