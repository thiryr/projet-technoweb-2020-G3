from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.fields.core import Field
from wtforms.fields.simple import FileField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.widgets.core import HTMLString, escape_html, html_params


class HelperTextWidget(object):
    """Custom widget that only displays a static text to use in forms"""

    def __call__(self, field: Field, **kwargs):
        return HTMLString(f'<span class="helper-text">{escape_html(field.description)}</span>')


class ButtonWidget(object):
    """Custom button widget used to create non-submit buttons"""
    outlined: bool = False
    href: str = ''
    onclick: str = ''
    submit: bool = False

    def __init__(self, outlined: bool = False, href: str = '', onclick: str = '', submit: bool = False):
        self.outlined = outlined
        self.href = href
        self.onclick = onclick
        self.submit = submit

    def __call__(self, field: Field, **kwargs):
        class_name = 'outlined-button' if self.outlined else 'filled-button'
        type_ = 'submit' if self.submit else False

        # Label of the button
        if self.href is None:
            element_name = 'button'
            params = html_params(
                class_=class_name, onclick=self.onclick, type=type_, **kwargs)
        else:
            element_name = 'a'
            params = html_params(
                class_=class_name, href=self.href, type=type_, **kwargs)

        html = f'<{element_name} {params}>{escape_html(field.label.text)}</{element_name}>'
        return HTMLString(html)


class SignInForm(FlaskForm):
    method = 'POST'
    title = 'Se connecter'

    # Username of the user
    username = StringField(
        label='Nom d\'utilisateur ou adresse email',
        validators=[InputRequired('Ce champ est obligatoire'),
                    Length(max=80, message="Le texte ne peut pas dépasser 80 caractères.")],
        render_kw={"placeholder": "john.doe@example.com"}

    )

    # Password of the user
    password = PasswordField(
        label='Mot de passe',
        description='Ceci est une description.',
        validators=[InputRequired('Ce champ est obligatoire'), ],
        render_kw={"placeholder": "azerty1234"}
    )

    submit = Field(
        widget=ButtonWidget(submit=True),
        label='Se connecter'
    )

    register = Field(
        widget=ButtonWidget(outlined=True, href='/register'),
        label='S\'inscrire',
    )


class RegisterForm(FlaskForm):
    method = 'POST'
    title = 'S\'inscrire'

    # Username of the user
    username = StringField(
        label='Nom d\'utilisateur',
        validators=[InputRequired('Ce champ est obligatoire'),
                    Length(max=80, message="Le texte ne peut pas dépasser 80 caractères.")],
        render_kw={"placeholder": "John12"}
    )

    # Password of the user
    password = PasswordField(
        label='Mot de passe',
        validators=[InputRequired('Ce champ est obligatoire'), ],
        render_kw={"placeholder": "azerty1234"}
    )

    confirm_password = PasswordField(
        label='Confirmer le mot de passe',
        validators=[InputRequired('Ce champ est obligatoire')],
        render_kw={"placeholder": "azerty1234"}
    )

    # Email of the user
    email = StringField(
        label='Adresse email',
        validators=[InputRequired('Ce champ est obligatoire')],
        render_kw={"placeholder": "john.doe@example.com"}
    )

    first_name = StringField(
        label='Prénom',
        render_kw={"placeholder": "John"}
    )

    last_name = StringField(
        label='Nom',
        render_kw={"placeholder": "Doe"}
    )

    # Use a StringField and validate manually (see below)
    birthday = StringField(
        label='Date de naissance',
        validators=[InputRequired('Ce champ est obligatoire'), ],
        description='Le format est JJ/MM/AAAA.',
        render_kw={"placeholder": "12/12/1980"}
    )

    # Text
    text = Field(
        widget=HelperTextWidget(),
        description='Si vous êtes un chef cuisinier, vous pouvez le signaler par courrier électronique à l\'administration du site (admin@coin-des-chefs.be) pour obtenir le status de chef. Ce status donne accès à diverses fonctionnalités supplémentaires. Une preuve sera demandée pour vérifier que vous êtes bien chef cuisinier.'
    )

    submit = Field(
        widget=ButtonWidget(submit=True),
        label='S\'inscrire'
    )

    # Custom validator for the birthday field
    # That way, we can customize the error message
    @staticmethod
    def validate_birthday(form, field):
        try:
            birthday = datetime.strptime(field.data, '%d/%m/%Y')
        except Exception:
            raise ValidationError(
                'Erreur : Date invalide. Le format est JJ/MM/AAAA.')

        if birthday >= datetime.now():
            raise ValidationError(
                'Erreur : Date invalide. La date doit être antérieure à aujourd\'hui.')

    # Validate second password : must be equal to the first one
    @staticmethod
    def validate_confirm_password(form, field):
        if field.data != form.password.data:
            raise ValidationError(
                'Erreur : Les deux mots de passe sont différents.')


class EditProfileForm(RegisterForm):
    title = 'Modifier le profil'

    # Password of the user
    password = PasswordField(
        label='Mot de passe',
        validators=[],
        render_kw={"placeholder": "azerty1234"}
    )

    confirm_password = PasswordField(
        label='Confirmer le mot de passe',
        validators=[],
        render_kw={"placeholder": "azerty1234"}
    )


    picture = FileField(
        label='Photo de profil'
    )

    text = None

    cancel = Field(
        widget=ButtonWidget(outlined=True, href="/profile"),
        label='Annuler'
    )

    submit = Field(
        widget=ButtonWidget(submit=True),
        label='Valider'
    )
