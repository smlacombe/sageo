from wtforms_components import PhoneNumberField
from wtforms_test import FormTestCase
from wtforms import Form
from tests import MultiDict


class TestPhoneNumberField(FormTestCase):
    def setup_method(self, method):
        self.valid_phone_numbers = [
            '040 1234567',
            '+358 401234567',
            '09 2501234',
            '+358 92501234',
            '0800 939393',
            '09 4243 0456',
            '0600 900 500'
        ]
        self.invalid_phone_numbers = [
            'abc',
            '+040 1234567',
            '0111234567',
            '358'
        ]

    def init_form(self, **kwargs):
        class ModelTestForm(Form):
            phone_number = PhoneNumberField(**kwargs)

        self.form_class = ModelTestForm
        return self.form_class

    def test_valid_phone_numbers(self):
        form_class = self.init_form(country_code='FI')
        for phone_number in self.valid_phone_numbers:
            form = form_class(MultiDict(phone_number=phone_number))
            form.validate()
            assert len(form.errors) == 0

    def test_invalid_phone_numbers(self):
        form_class = self.init_form(country_code='FI')
        for phone_number in self.invalid_phone_numbers:
            form = form_class(MultiDict(phone_number=phone_number))
            form.validate()
            assert len(form.errors['phone_number']) == 1

    def test_render_empty_phone_number_value(self):
        form_class = self.init_form(country_code='FI')
        form = form_class(MultiDict(phone_number=''))
        assert 'value=""' in form.phone_number()

    def test_empty_phone_number_value_passed_as_none(self):
        form_class = self.init_form(country_code='FI')
        form = form_class(MultiDict(phone_number=''))
        form.validate()
        assert len(form.errors) == 0
        assert form.data['phone_number'] is None

    def test_default_display_format(self):
        form_class = self.init_form(country_code='FI')
        form = form_class(MultiDict(phone_number='+358401234567'))
        assert 'value="040 1234567"' in form.phone_number()

    def test_international_display_format(self):
        form_class = self.init_form(
            country_code='FI',
            display_format='international'
        )
        form = form_class(MultiDict(phone_number='0401234567'))
        assert 'value="+358 40 1234567"' in form.phone_number()

    def test_e164_display_format(self):
        form_class = self.init_form(
            country_code='FI',
            display_format='e164'
        )
        form = form_class(MultiDict(phone_number='0401234567'))
        assert 'value="+358401234567"' in form.phone_number()

    def test_field_rendering_when_invalid_phone_number(self):
        form_class = self.init_form()
        form = form_class(MultiDict(phone_number='invalid'))
        form.validate()
        assert 'value="invalid"' in form.phone_number()
