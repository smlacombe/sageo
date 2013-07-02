import re
from wtforms import ValidationError
from wtforms.validators import StopValidation


class ControlStructure(object):
    """
    Base object for validator control structures
    """

    message = None

    def reraise(self, exc):
        if not self.message:
            raise exc
        else:
            raise type(exc)(self.message)


class Chain(ControlStructure):
    """
    Represents a chain of validators, useful when using multiple validators
    with If control structure.

    :param validators:
        list of validator objects
    :param message:
        custom validation error message, if this message is set and some of the
        child validators raise a ValidationError, an exception is being raised
        again with this custom message.
    """
    def __init__(self, validators, message=None):
        self.validators = validators
        if message:
            self.message = message

    def __call__(self, form, field):
        for validator in self.validators:
            try:
                validator(form, field)
            except ValidationError, exc:
                self.reraise(exc)
            except StopValidation, exc:
                self.reraise(exc)


class If(ControlStructure):
    """
    Conditional validator.

    :param condition: callable which takes two arguments form and field
    :param validator: encapsulated validator, this validator is validated
                      only if given condition returns true
    :param message: custom message, which overrides child validator's
                    validation error message
    """
    def __init__(self, condition, validator, message=None):
        self.condition = condition
        self.validator = validator

        if message:
            self.message = message

    def __call__(self, form, field):
        if self.condition(form, field):
            try:
                self.validator(form, field)
            except ValidationError, exc:
                self.reraise(exc)
            except StopValidation, exc:
                self.reraise(exc)


class BaseDateTimeRange(object):
    def __init__(self, min=None, max=None, format='%H:%M', message=None):
        self.min = min
        self.max = max
        self.format = format
        self.message = message

    def __call__(self, form, field):
        data = field.data
        min_ = self.min() if callable(self.min) else self.min
        max_ = self.max() if callable(self.max) else self.max
        if (data is None or (min_ is not None and data < min_) or
                (max_ is not None and data > max_)):
            if self.message is None:
                if max_ is None:
                    self.message = field.gettext(self.greater_than_msg)
                elif min_ is None:
                    self.message = field.gettext(self.less_than_msg)
                else:
                    self.message = field.gettext(self.between_msg)

            raise ValidationError(
                self.message % dict(
                    field_label=field.label,
                    min=min_.strftime(self.format) if min_ else '',
                    max=max_.strftime(self.format) if max_ else ''
                )
            )


class TimeRange(BaseDateTimeRange):
    """
    Same as wtforms.validators.NumberRange but validates date.

    :param min:
        The minimum required value of the time. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the time. If not provided, maximum value
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)s` and `%(max)s` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """

    greater_than_msg = u'Time must be greater than %(min)s.'

    less_than_msg = u'Time must be less than %(max)s.'

    between_msg = u'Time must be between %(min)s and %(max)s.'

    def __init__(self, min=None, max=None, format='%H:%M', message=None):
        super(TimeRange, self).__init__(
            min=min, max=max, format=format, message=message
        )


class DateRange(BaseDateTimeRange):
    """
    Same as wtforms.validators.NumberRange but validates date.

    :param min:
        The minimum required value of the date. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the date. If not provided, maximum value
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)s` and `%(max)s` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """

    greater_than_msg = u'Date must be greater than %(min)s.'

    less_than_msg = u'Date must be less than %(max)s.'

    between_msg = u'Date must be between %(min)s and %(max)s.'

    def __init__(self, min=None, max=None, format='%Y-%m-%d', message=None):
        super(DateRange, self).__init__(
            min=min, max=max, format=format, message=message
        )


class Unique(object):
    """Checks field value unicity against specified table field.

    :param column:
        InstrumentedAttribute object, eg. User.name
    :param get_session:
        A function that returns a SQAlchemy Session. This parameter is not
        needed if the given model supports Flask-SQLAlchemy styled query
        parameter.
    :param message:
        The error message.
    """
    field_flags = ('unique', )

    def __init__(self, column, get_session=None, message=None):
        self.model = column.class_
        self.column = column
        self.message = message
        self.get_session = get_session

        if not hasattr(self.model, 'query') and not get_session:
            raise Exception('Could not obtain SQLAlchemy session.')

    @property
    def query(self):
        if hasattr(self.model, 'query'):
            return getattr(self.model, 'query')
        return self.get_session().query(self.model)

    def __call__(self, form, field):
        obj = (
            self.query
            .filter(self.column == field.data).first()
        )

        if not hasattr(form, '_obj') or (obj and not form._obj == obj):
            if self.message is None:
                self.message = field.gettext(u'Already exists.')
            raise ValidationError(self.message)


class Email(object):
    """
    Validates an email address. This validator is based on `Django's
    email validator`_ and is stricter than the standard email
    validator included in WTForms.

    .. _Django's email validator:
       https://github.com/django/django/blob/master/django/core/validators.py

    :param message:
        Error message to raise in case of a validation error.

    :copyright: (c) Django Software Foundation and individual contributors.
    :license: BSD
    """
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)',  # quoted-string
        re.IGNORECASE)
    domain_regex = re.compile(
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?$)'  # domain
        # literal form, ipv4 address (SMTP 4.1.3)
        r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    def __init__(self, message=None, whitelist=None):
        self.message = message
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def __call__(self, form, field):
        if self.message is None:
            self.message = field.gettext('Invalid email address.')

        value = field.data or ''

        if not value or '@' not in value:
            raise ValidationError(self.message)

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message)

        if (not domain_part in self.domain_whitelist and
                not self.domain_regex.match(domain_part)):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode('idna').decode('ascii')
                if not self.domain_regex.match(domain_part):
                    raise ValidationError(self.message)
                else:
                    return
            except UnicodeError:
                pass
            raise ValidationError(self.message)
