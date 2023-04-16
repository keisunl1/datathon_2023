from wtforms import Form, validators, SubmitField, SelectMultipleField

class ReusableForm(Form):
    # Year Selector
    year = SelectMultipleField("Select Year: ", choices=[('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'),\
                                                 ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023')], validators=[validators.InputRequired()])
    # Time Selector
    time = SelectMultipleField("Select Time: ", choices=[('Day', 'Day (8:01 a.m. to 4:00 p.m.)'), ('Evening', 'Evening (4:01 p.m. to midnight)'),\
                                                         ('Night', 'Night (Midnight to 8:00 a.m.)')], validators=[validators.InputRequired()])
    
    # Submit button
    submit = SubmitField("Submit")
