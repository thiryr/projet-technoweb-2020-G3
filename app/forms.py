from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length


class SignInForm(FlaskForm):

    # Username of the user
    username = StringField(
        label='Nom d\'utilisateur',
        validators=[InputRequired('Ce champ est obligatoire'),
                    Length(max=80, message="Le texte ne peut pas dépasser 80 caractères.")],
    )

    # Password of the user
    password = PasswordField(
        label='Mot de passe',
        validators=[InputRequired('Ce champ est obligatoire'), ]
    )

    submit = SubmitField('Se connecter')
