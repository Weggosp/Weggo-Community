"""
<!-- -| 
  
  * WEGGO is a registered trademark in Spain as Plataforma Weggo Espana, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class confirmAccount(FlaskForm):
    fullname = StringField('Nombre y apellidos', validators=[DataRequired(message='Por favor, introduce el primer nombre.'), Length(min=10, max=50)])
    email = StringField('Email', validators=[DataRequired(message='Por favor, introduce un email válido.'), Length(min=7, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Por favor, introduce un email válido.'), Length(min=7, max=50)])
    submit = SubmitField('Submit')

class NewsletterForm(FlaskForm):
    email = StringField('Email Newsletter', validators=[DataRequired(), Email()])

    
from wtforms.fields import DateField,TextAreaField
class ReserverForm(FlaskForm):
    startdate = DateField('Start Date', format='%d-%m-%Y', validators=[DataRequired()])
    enddate = DateField('End Date', format='%d-%m-%Y', validators=[DataRequired()])
    submit = SubmitField('Submit')


class QueryForm(FlaskForm):
    fullname = StringField('Fecha de la reserva', validators=[DataRequired(message='Por favor, introduce el primer nombre.'), Length(min=10, max=50)])
    email = StringField('Fecha de la reserva', validators=[DataRequired(message='Por favor, introduce un email válido.'), Length(min=7, max=50)])
    phone = StringField('Fecha de la reserva', validators=[DataRequired(message='Por favor, introduce un teléfono válido.'), Length(min=8, max=12)])
    content = TextAreaField('Pregunta del cliente')
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    name = StringField('nombre', validators=[DataRequired()])
    lastname = StringField('apellido', validators=[DataRequired()])
    title = StringField('titulo', validators=[DataRequired()])
    score = StringField('Puntuación', validators=[DataRequired()])
    content = StringField('Comentario')
