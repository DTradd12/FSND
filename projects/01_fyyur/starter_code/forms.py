from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL


class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id'
    )
    venue_id = IntegerField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired()]
    )
    website_link = StringField(
        'website_link', validators=[URL()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    seeking_talent = SelectField(
        'seeking_talent', validators=[DataRequired()],
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ]
    )
    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[DataRequired()]
    )
    genres = SelectMultipleField(

        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    available_times = SelectMultipleField(

        'availabile_times', validators=[DataRequired()],
        choices=[
            ('00:00:00', '12:00 AM'),
            ('00:30:00', '12:30 AM'),
            ('01:00:00', '1:00 AM'),
            ('01:30:00', '1:30 AM'),
            ('02:00:00', '2:00 AM'),
            ('02:30:00', '2:30 AM'),
            ('03:00:00', '3:00 AM'),
            ('03:30:00', '3:30 AM'),
            ('04:00:00', '4:00 AM'),
            ('04:30:00', '4:30 AM'),
            ('05:00:00', '5:00 AM'),
            ('05:30:00', '5:30 AM'),
            ('06:00:00', '6:00 AM'),
            ('06:30:00', '6:30 AM'),
            ('07:00:00', '7:00 AM'),
            ('07:30:00', '7:30 AM'),
            ('08:00:00', '8:00 AM'),
            ('08:30:00', '8:30 AM'),
            ('09:00:00', '9:00 AM'),
            ('09:30:00', '9:30 AM'),
            ('10:00:00', '10:00 AM'),
            ('10:30:00', '10:30 AM'),
            ('11:00:00', '11:00 AM'),
            ('11:30:00', '11:30 AM'),
            ('12:00:00', '12:00 PM'),
            ('12:30:00', '12:30 PM'),
            ('13:00:00', '1:00 PM'),
            ('13:30:00', '1:30 PM'),
            ('14:00:00', '2:00 PM'),
            ('14:30:00', '2:30 PM'),
            ('15:00:00', '3:00 PM'),
            ('15:30:00', '3:30 PM'),
            ('16:00:00', '4:00 PM'),
            ('16:30:00', '4:30 PM'),
            ('17:00:00', '5:00 PM'),
            ('17:30:00', '5:30 PM'),
            ('18:00:00', '6:00 PM'),
            ('18:30:00', '6:30 PM'),
            ('19:00:00', '7:00 PM'),
            ('19:30:00', '7:30 PM'),
            ('20:00:00', '8:00 PM'),
            ('20:30:00', '8:30 PM'),
            ('21:00:00', '9:00 PM'),
            ('21:30:00', '9:30 PM'),
            ('22:00:00', '10:00 PM'),
            ('22:30:00', '10:30 PM'),
            ('13:00:00', '11:00 PM'),
            ('13:30:00', '11:30 PM'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link', validators=[URL()]
    )
    seeking_perf = SelectField(
        'seeking_perf', validators=[DataRequired()],
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ]
    )
    seeking_description = StringField(
        'seeking_description'
    )
