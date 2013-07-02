from decimal import Decimal
import sqlalchemy as sa
from wtforms_alchemy import SelectField
from tests import ModelFormTestCase


class MultiDict(dict):
    def getlist(self, key):
        return [self[key]]


class TestSelectFieldCoerce(ModelFormTestCase):
    def test_integer_coerces_values_to_integers(self):
        choices = [(u'1', '1'), (u'2', '2')]
        self.init(type_=sa.Integer, info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': '2'}))
        assert form.test_column.data is 2

    def test_nullable_integer_coerces_values_to_integers(self):
        choices = [(u'1', '1'), (u'2', '2')]
        self.init(type_=sa.Integer, nullable=True, info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': '2'}))
        assert form.test_column.data is 2

    def test_integer_coerces_empty_strings_to_nulls(self):
        choices = [(u'1', '1'), (u'2', '2')]
        self.init(type_=sa.Integer, info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': ''}))
        assert form.test_column.data is None

    def test_big_integer_coerces_values_to_integers(self):
        choices = [(u'1', '1'), (u'2', '2')]
        self.init(type_=sa.BigInteger, info={'choices': choices})
        self.assert_type('test_column', SelectField)
        form = self.form_class(MultiDict({'test_column': '2'}))
        assert form.test_column.data is 2

    def test_small_integer_coerces_values_to_integers(self):
        choices = [(u'1', '1'), (u'2', '2')]
        self.init(type_=sa.SmallInteger, info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': '2'}))
        assert form.test_column.data is 2

    def test_numeric_coerces_values_to_decimals(self):
        choices = [(u'1.0', '1.0'), (u'2.0', '2.0')]
        self.init(type_=sa.Numeric, info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': '2.0'}))
        assert form.test_column.data == Decimal('2.0')

    def test_float_coerces_values_to_floats(self):
        choices = [(u'1.0', '1.0'), (u'2.0', '2.0')]
        self.init(type_=sa.Float, info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': '2.0'}))
        assert form.test_column.data == 2.0

    def test_unicode_coerces_values_to_unicode_strings(self):
        choices = [('1.0', '1.0'), ('2.0', '2.0')]
        self.init(type_=sa.Unicode(255), info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': '2.0'}))
        assert form.test_column.data == u'2.0'
        assert isinstance(form.test_column.data, unicode)

    def test_unicode_text_coerces_values_to_unicode_strings(self):
        choices = [('1.0', '1.0'), ('2.0', '2.0')]
        self.init(type_=sa.UnicodeText, info={'choices': choices})
        form = self.form_class(MultiDict({'test_column': '2.0'}))
        assert form.test_column.data == u'2.0'
        assert isinstance(form.test_column.data, unicode)
