"""
<!-- -| 
  
  * WEGGO INTERNATIONAL is a registered trademark in Spain by WEGGO as Plataforma Weggo Espana, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

# Mailing
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class emails:
    def welcome_ceo_message(user,subject,html):
        message = Mail(
            from_email='ceo@weggo.es',
            to_emails=user['email'],
            subject=subject,
            html_content=html
            )
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    def send_auth_emails(user,subject1,html1):
        message = Mail(
        #from_email='no-reply@send-emails.weggot.com',
        from_email='info@weggo.es',
        to_emails=user['email'],
        subject=subject1,
        html_content=html1
        )
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)


    def send_public_emails(email,subject1,html1):
        message = Mail(
        from_email='info@weggo.es',
        to_emails=email,
        subject=subject1,
        html_content=html1
        )
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    def send_account_confirm_from_public(email,subject,html):
        message = Mail(
        from_email='info@weggo.es',
        to_emails=email,
        subject=subject,
        html_content=html
        )
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    def confirm_register(user):

        # Configuración de la cuenta saliente
        anfitrion = "smtp.ionos.es" # Servidor Ionos
        #anfitrion = "email-smtp.eu-west-1.amazonaws.com" # Servidor AWS
        puerto = 587
        #direccionDe = "info@strusiness.weggo.com" # Servidor Ionos
        direccionDe = "info@weggo.es" # Servidor AWS
        contrasenaDe = "Info_WeGgO?p.access070721"
        direccionPara = user.email # Para quien

        # Creación del mensaje
        em = EmailMessage()

        asunto = "Confirmación de registro | Weggo España"
        em['From'] = direccionDe
        em['To'] = direccionPara
        em['Subject'] = asunto

        if user.is_user == True:
            message = "Estimado "+str(user.name)+",\n\nLe confirmamos los datos con los que se ha registrado en nuestra plataforma.\n\n Datos de acceso:\n\n Correo electrónico: "+str(user.email)+"\n  Nombre: "+str(user.name)+"\n  Apellidos: "+str(user.lastname)+"\n\nGracias por unirse a nuestra comunidad. Mejoramos cada día para ofrecerle la mejor experiencia con nosotros.\n\nUn saludo,\nel equipo de Weggo."
            em.set_content(message)

        if user.is_coll == True:
            conn = engine.connect()
            users_stripe = conn.execute('SELECT * FROM users_stripe').fetchall()
            for info in users_stripe:
                if info.userid == user.userid:
                    if info.type == 'company':
                        message = "Estimado "+str(user.name)+",\n\nLe confirmamos que usted se ha registrado cómo EMPRESA (entidad jurídica). Compartimos los datos con los que se ha registrado en nuestra plataforma.\n\n Datos de acceso:\n\n  Correo electrónico: "+str(user.email)+"\n  Nombre: "+str(user.name)+"\n  Apellidos: "+str(user.lastname)+"\n\nGracias por colaborar con nuestra comunidad. Recuerda modificar los datos en su perfil ya que dispone de un período de 15 días para completar los datos básicos.\n\nMejoramos cada día para ofrecerte el mayor valor posible para sus negocios en nuestra plataforma y que esta sea de su agrado.\n\nAtentamente,\nel equipo de Weggo."
                        em.set_content(message)

                    elif info.type == 'individual':
                        message = "Estimado "+str(user.name)+",\n\nLe confirmamos que usted se ha registrado cómo PROFESIONAL PARTICULAR. Compartimos los datos con los que se ha registrado en nuestra plataforma.\n\n Datos de acceso:\n\n  ID de usuario: "+str(user.userid)+"\n Correo electrónico: "+str(user.email)+"\n  Nombre: "+str(user.name)+"\n  Apellidos: "+str(user.lastname)+"\n Nombre comercial: "+str(info.name)+"\n\nGracias por colaborar con nuestra comunidad. Recuerda modificar los datos en su perfil ya que dispone de un período de 15 días para completar los datos básicos.\n\nMejoramos cada día para ofrecerte el mayor valor posible para sus negocios en nuestra plataforma y que esta sea de su agrado.\n\nAtentamente,\nel equipo de Weggo."
                        em.set_content(message)
            conn.close()
        # Configuración del servidor de correo
        servidor = smtplib.SMTP(anfitrion,puerto)
        servidor.starttls()
        servidor.login(direccionDe,contrasenaDe) # Servidor Ionos
        #servidor.login("AKIAQUZST2T2XK3VUPXW","BBJowl3alwdnt3yH8qV+3OOMNpPCXbHhD1UbDNdDTvtJ") # Servidor AWS
        servidor.send_message(em)

    def reset_password(user, subject, html, password):
        from flask_mail import Message
        from app import mail
        fromEmail = "info@weggo.es" # Servidor AWS
        # Create the message
        msg = Message(subject,
                sender=fromEmail,
                recipients=[user.email])

        if user.is_user == True:
            msg.html = html.format(user.name,user.lastname,password)
            #"Estimado "+str(user.name)+",\n\nLe confirmamos los datos con los que se ha registrado en nuestra plataforma.\n\n Datos de acceso:\n\n Correo electrónico: "+str(user.email)+"\n  Nombre: "+str(user.name)+"\n  Apellidos: "+str(user.lastname)+"\n\nGracias por unirse a nuestra comunidad. Mejoramos cada día para ofrecerle la mejor experiencia con nosotros.\n\nUn saludo,\nel equipo de Weggo."
            mail.send(msg)

    def send_newsletter_confirmation(req_email, subject, html):
        message = Mail(
            from_email='info@weggo.es',
            to_emails=req_email,
            subject=subject,
            html_content=html
            )
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    ## Confirmación de reservas
    def enviar_confirmacion_reserva_user(oferta,usuario,oferente,fecha_ini,fecha_fin):
        # Configuración de la cuenta saliente
        anfitrion = "smtp.ionos.es" # Servidor Ionos
        #anfitrion = "email-smtp.eu-west-1.amazonaws.com" # Servidor AWS
        puerto = 587
        #direccionDe = "info@strusiness.weggo.com" # Servidor Ionos
        direccionDe = "info@weggo.es" # Servidor AWS
        contrasenaDe = "Info_WeGgO?p.access070721"
        direccionPara = usuario.email # Para quien

        # Creación del mensaje
        em = EmailMessage()

        asunto = "INFORMACION SOBRE SU RESERVA EN WEGGO"
        em['From'] = direccionDe
        em['To'] = direccionPara
        em['Subject'] = asunto

        message = "Estimado "+str(usuario.name)+",\n\nse ha realizado una petición de reserva para la oferta \""+str(oferta.titulo)+"\" por su parte a través de Weggo España con fecha de inicio el "+str(fecha_ini)+" y fecha de finalización el "+str(fecha_fin)+". El anunciante se pondrá en contacto contigo para confirmarla y realizar el pago en menos de 24h.\n\nUn saludo,\nel equipo de Weggo."
        em.set_content(message)

        # Configuración del servidor de correo
        servidor = smtplib.SMTP(anfitrion,puerto)
        servidor.starttls()
        servidor.login(direccionDe,contrasenaDe) # Servidor Ionos
        #servidor.login("AKIAQUZST2T2XK3VUPXW","BBJowl3alwdnt3yH8qV+3OOMNpPCXbHhD1UbDNdDTvtJ") # Servidor AWS
        servidor.send_message(em)

    def enviar_confirmacion_reserva_col(oferta,usuario,oferente,fecha_ini,fecha_fin):
        # Configuración de la cuenta saliente
        anfitrion = "smtp.ionos.es" # Servidor Ionos
        #anfitrion = "email-smtp.eu-west-1.amazonaws.com" # Servidor AWS
        puerto = 587
        #direccionDe = "info@strusiness.weggo.com" # Servidor Ionos
        direccionDe = "info@weggo.es" # Servidor AWS
        contrasenaDe = "Info_WeGgO?p.access070721"
        direccionPara = oferente.email # Para quien

        # Creación del mensaje
        em = EmailMessage()

        asunto = "HA RECIBIDO UNA PETICIÓN DE RESERVA A TRAVÉS DE WEGGO"
        em['From'] = direccionDe
        em['To'] = direccionPara
        em['Subject'] = asunto

        message = "Estimado "+str(oferente.name)+", \n\nel usuario "+str(usuario.name)+" ha realizado una solicitud de reserva por su oferta \""+str(oferta.titulo)+"\" a través de Weggo con fecha de inicio el "+str(fecha_ini)+" y fecha de finalización el "+str(fecha_fin)+". Por favor, póngase en contacto con el usuario a través de la dirección de correo "+str(usuario.email)+" en las próximas 24h para confirmar la reserva y recibir el pago.\n\n Un saludo,\nel equipo de Weggo."
        em.set_content(message)

        # Configuración del servidor de correo
        servidor = smtplib.SMTP(anfitrion,puerto)
        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()
        servidor.login(direccionDe,contrasenaDe) # Servidor Ionos
        # servidor.login("AKIAQUZST2T2XK3VUPXW","BBJowl3alwdnt3yH8qV+3OOMNpPCXbHhD1UbDNdDTvtJ") # Servidor AWS
        servidor.send_message(em)
        servidor.close()

