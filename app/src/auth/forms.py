"""
<!-- -| 
  
  * WEGGO is a registered trademark in Spain as Plataforma Weggo Espana, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Email

class SavedCookies(FlaskForm):
    id = HiddenField()
    quantity = IntegerField('Cantidad', default=1,
                            validators=[NumberRange(min=1,
                                                    message="Debe ser un núme"
                                                            "ro positivo"),
                                        DataRequired("Tienes que introducir el "
                                                 "dato")])
    submit = SubmitField('Aceptar')

class UserSignup(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])

    submit = SubmitField('Register')

class SupplierSignup(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])

class SupplierSignup2(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(max=80)])
    day = StringField('Day of born', validators=[DataRequired(), Length(max=80)])
    month = StringField('Month of born', validators=[DataRequired(), Length(max=80)])
    year = StringField('Year of born', validators=[DataRequired(), Length(max=80)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=80)])
    cif = StringField('Cif', validators=[DataRequired(), Length(max=9)])
    business_name = StringField('Business name', validators=[DataRequired(), Length(max=80)])
    type = StringField('Type of business', validators=[DataRequired(), Length(max=80)])
    ind = StringField('Industry', validators=[DataRequired(), Length(max=80)])
    web = StringField('Website', validators=[DataRequired(), Length(max=80)])
    dir = StringField('Direccion', validators=[DataRequired(), Length(max=80)])
    city = StringField('City', validators=[DataRequired(), Length(max=80)])
    province = StringField('Province', validators=[DataRequired(), Length(max=80)])
    zip = StringField('Zip', validators=[DataRequired(), Length(max=80)])

    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Correo electrónico o nombre de usuario', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=20)])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Conectarme')
