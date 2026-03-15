"""
WTForms for Modern Online Store
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, URL
from models import User


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Create Account')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another.')


class ProfileForm(FlaskForm):
    """Profile update form"""
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Update Profile')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != self.current_user_id:
            raise ValidationError('Email already in use by another account.')


class ChangePasswordForm(FlaskForm):
    """Change password form"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class AddressForm(FlaskForm):
    """Address form"""
    address_type = SelectField('Address Type', choices=[('shipping', 'Shipping'), ('billing', 'Billing')])
    street_address = StringField('Street Address', validators=[DataRequired(), Length(max=255)])
    address_line2 = StringField('Address Line 2 (Optional)', validators=[Optional(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    province = StringField('Province', validators=[Optional(), Length(max=100)])
    state = StringField('State/Region', validators=[Optional(), Length(max=100)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)], default='South Africa')
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    is_default = BooleanField('Set as Default Address')
    submit = SubmitField('Save Address')


class ProductForm(FlaskForm):
    """Admin product form"""
    name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (ZAR)', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Electronics', 'Electronics'),
        ('Accessories', 'Accessories'),
        ('Bags', 'Bags'),
        ('Footwear', 'Footwear'),
        ('Clothing', 'Clothing'),
        ('Home', 'Home'),
        ('Other', 'Other')
    ])
    image = StringField('Image URL', validators=[Optional(), URL()])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired()])
    weight_kg = FloatField('Weight (kg)', validators=[Optional()])
    is_featured = BooleanField('Featured Product')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Product')


class OrderStatusForm(FlaskForm):
    """Admin order status update form"""
    status = SelectField('Order Status', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ])
    payment_status = SelectField('Payment Status', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed')
    ])
    notes = TextAreaField('Order Notes')
    submit = SubmitField('Update Order')


class ShippingZoneForm(FlaskForm):
    """Admin shipping zone form"""
    name = StringField('Zone Name', validators=[DataRequired()])
    code = StringField('Zone Code', validators=[DataRequired(), Length(max=50)])
    regions = TextAreaField('Regions (comma separated)')
    base_rate = FloatField('Base Rate (ZAR)', validators=[DataRequired()])
    per_kg_rate = FloatField('Per kg Rate (ZAR)', validators=[DataRequired()])
    estimated_days = StringField('Estimated Delivery Days', validators=[Optional()])
    submit = SubmitField('Save Zone')
