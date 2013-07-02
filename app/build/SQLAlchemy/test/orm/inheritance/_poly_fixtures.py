from sqlalchemy import Integer, String, ForeignKey, func, desc, and_, or_
from sqlalchemy.orm import interfaces, relationship, mapper, \
    clear_mappers, create_session, joinedload, joinedload_all, \
    subqueryload, subqueryload_all, polymorphic_union, aliased,\
    class_mapper
from sqlalchemy import exc as sa_exc
from sqlalchemy.engine import default

from sqlalchemy.testing import AssertsCompiledSQL, fixtures
from sqlalchemy import testing
from sqlalchemy.testing.schema import Table, Column
from sqlalchemy.testing import assert_raises, eq_

class Company(fixtures.ComparableEntity):
    pass
class Person(fixtures.ComparableEntity):
    pass
class Engineer(Person):
    pass
class Manager(Person):
    pass
class Boss(Manager):
    pass
class Machine(fixtures.ComparableEntity):
    pass
class Paperwork(fixtures.ComparableEntity):
    pass


class _PolymorphicFixtureBase(fixtures.MappedTest, AssertsCompiledSQL):
    run_inserts = 'once'
    run_setup_mappers = 'once'
    run_deletes = None

    @classmethod
    def define_tables(cls, metadata):
        global people, engineers, managers, boss
        global companies, paperwork, machines

        companies = Table('companies', metadata,
            Column('company_id', Integer,
                primary_key=True,
                test_needs_autoincrement=True),
            Column('name', String(50)))

        people = Table('people', metadata,
            Column('person_id', Integer,
                primary_key=True,
                test_needs_autoincrement=True),
            Column('company_id', Integer,
                ForeignKey('companies.company_id')),
            Column('name', String(50)),
            Column('type', String(30)))

        engineers = Table('engineers', metadata,
            Column('person_id', Integer,
                ForeignKey('people.person_id'),
                primary_key=True),
            Column('status', String(30)),
            Column('engineer_name', String(50)),
            Column('primary_language', String(50)))

        machines = Table('machines', metadata,
             Column('machine_id',
                 Integer, primary_key=True,
                 test_needs_autoincrement=True),
             Column('name', String(50)),
             Column('engineer_id', Integer,
            ForeignKey('engineers.person_id')))

        managers = Table('managers', metadata,
            Column('person_id', Integer,
                ForeignKey('people.person_id'),
                primary_key=True),
            Column('status', String(30)),
            Column('manager_name', String(50)))

        boss = Table('boss', metadata,
            Column('boss_id', Integer,
                ForeignKey('managers.person_id'),
                primary_key=True),
            Column('golf_swing', String(30)))

        paperwork = Table('paperwork', metadata,
            Column('paperwork_id', Integer,
                primary_key=True,
                test_needs_autoincrement=True),
            Column('description', String(50)),
            Column('person_id', Integer,
                ForeignKey('people.person_id')))

    @classmethod
    def insert_data(cls):

        cls.e1 = e1 = Engineer(
            name="dilbert",
            engineer_name="dilbert",
            primary_language="java",
            status="regular engineer",
            paperwork=[
                Paperwork(description="tps report #1"),
                Paperwork(description="tps report #2")],
            machines=[
                Machine(name='IBM ThinkPad'),
                Machine(name='IPhone')])

        cls.e2 = e2 = Engineer(
            name="wally",
            engineer_name="wally",
            primary_language="c++",
            status="regular engineer",
            paperwork=[
                Paperwork(description="tps report #3"),
                Paperwork(description="tps report #4")],
            machines=[Machine(name="Commodore 64")])

        cls.b1 = b1 = Boss(
            name="pointy haired boss",
            golf_swing="fore",
            manager_name="pointy",
            status="da boss",
            paperwork=[Paperwork(description="review #1")])

        cls.m1 = m1 = Manager(
            name="dogbert",
            manager_name="dogbert",
            status="regular manager",
            paperwork=[
                Paperwork(description="review #2"),
                Paperwork(description="review #3")])

        cls.e3 = e3 = Engineer(
            name="vlad",
            engineer_name="vlad",
            primary_language="cobol",
            status="elbonian engineer",
            paperwork=[
                Paperwork(description='elbonian missive #3')],
            machines=[
                Machine(name="Commodore 64"),
                Machine(name="IBM 3270")])

        cls.c1 = c1 = Company(name="MegaCorp, Inc.")
        c1.employees = [e1, e2, b1, m1]
        cls.c2 = c2 = Company(name="Elbonia, Inc.")
        c2.employees = [e3]

        sess = create_session()
        sess.add(c1)
        sess.add(c2)
        sess.flush()
        sess.expunge_all()

        cls.all_employees = [e1, e2, b1, m1, e3]
        cls.c1_employees = [e1, e2, b1, m1]
        cls.c2_employees = [e3]

    def _company_with_emps_machines_fixture(self):
        fixture = self._company_with_emps_fixture()
        fixture[0].employees[0].machines = [
            Machine(name="IBM ThinkPad"),
            Machine(name="IPhone"),
        ]
        fixture[0].employees[1].machines = [
            Machine(name="Commodore 64")
        ]
        return fixture

    def _company_with_emps_fixture(self):
        return [
            Company(
                name="MegaCorp, Inc.",
                employees=[
                    Engineer(
                        name="dilbert",
                        engineer_name="dilbert",
                        primary_language="java",
                        status="regular engineer"
                    ),
                    Engineer(
                        name="wally",
                        engineer_name="wally",
                        primary_language="c++",
                        status="regular engineer"),
                    Boss(
                        name="pointy haired boss",
                        golf_swing="fore",
                        manager_name="pointy",
                        status="da boss"),
                    Manager(
                        name="dogbert",
                        manager_name="dogbert",
                        status="regular manager"),
                ]),
            Company(
                name="Elbonia, Inc.",
                employees=[
                    Engineer(
                        name="vlad",
                        engineer_name="vlad",
                        primary_language="cobol",
                        status="elbonian engineer")
                ])
        ]

    def _emps_wo_relationships_fixture(self):
        return [
            Engineer(
                name="dilbert",
                engineer_name="dilbert",
                primary_language="java",
                status="regular engineer"),
            Engineer(
                name="wally",
                engineer_name="wally",
                primary_language="c++",
                status="regular engineer"),
            Boss(
                name="pointy haired boss",
                golf_swing="fore",
                manager_name="pointy",
                status="da boss"),
            Manager(
                name="dogbert",
                manager_name="dogbert",
                status="regular manager"),
            Engineer(
                name="vlad",
                engineer_name="vlad",
                primary_language="cobol",
                status="elbonian engineer")
        ]

    @classmethod
    def setup_mappers(cls):
        mapper(Company, companies,
            properties={
                'employees':relationship(
                    Person,
                    order_by=people.c.person_id)})

        mapper(Machine, machines)

        person_with_polymorphic,\
            manager_with_polymorphic = cls._get_polymorphics()

        mapper(Person, people,
            with_polymorphic=person_with_polymorphic,
            polymorphic_on=people.c.type,
            polymorphic_identity='person',
            order_by=people.c.person_id,
            properties={
                'paperwork':relationship(
                    Paperwork,
                    order_by=paperwork.c.paperwork_id)})

        mapper(Engineer, engineers,
            inherits=Person,
            polymorphic_identity='engineer',
            properties={
                'machines':relationship(
                    Machine,
                    order_by=machines.c.machine_id)})

        mapper(Manager, managers,
            with_polymorphic=manager_with_polymorphic,
            inherits=Person,
            polymorphic_identity='manager')

        mapper(Boss, boss,
            inherits=Manager,
            polymorphic_identity='boss')

        mapper(Paperwork, paperwork)

class _Polymorphic(_PolymorphicFixtureBase):
    select_type = ""
    @classmethod
    def _get_polymorphics(cls):
        return None, None

class _PolymorphicPolymorphic(_PolymorphicFixtureBase):
    select_type = "Polymorphic"
    @classmethod
    def _get_polymorphics(cls):
        return '*', '*'


class _PolymorphicUnions(_PolymorphicFixtureBase):
    select_type = "Unions"

    @classmethod
    def _get_polymorphics(cls):
        people, engineers, managers, boss = \
            cls.tables.people, cls.tables.engineers, \
            cls.tables.managers, cls.tables.boss
        person_join = polymorphic_union({
                'engineer':people.join(engineers),
                'manager':people.join(managers)},
            None, 'pjoin')
        manager_join = people.join(managers).outerjoin(boss)
        person_with_polymorphic = (
            [Person, Manager, Engineer], person_join)
        manager_with_polymorphic = ('*', manager_join)
        return person_with_polymorphic,\
            manager_with_polymorphic


class _PolymorphicAliasedJoins(_PolymorphicFixtureBase):
    select_type = "AliasedJoins"

    @classmethod
    def _get_polymorphics(cls):
        people, engineers, managers, boss = \
            cls.tables.people, cls.tables.engineers, \
            cls.tables.managers, cls.tables.boss
        person_join = people \
            .outerjoin(engineers) \
            .outerjoin(managers) \
            .select(use_labels=True) \
            .alias('pjoin')
        manager_join = people \
            .join(managers) \
            .outerjoin(boss) \
            .select(use_labels=True) \
            .alias('mjoin')
        person_with_polymorphic = (
            [Person, Manager, Engineer], person_join)
        manager_with_polymorphic = ('*', manager_join)
        return person_with_polymorphic,\
            manager_with_polymorphic


class _PolymorphicJoins(_PolymorphicFixtureBase):
    select_type = "Joins"

    @classmethod
    def _get_polymorphics(cls):
        people, engineers, managers, boss = \
            cls.tables.people, cls.tables.engineers, \
            cls.tables.managers, cls.tables.boss
        person_join = people.outerjoin(engineers).outerjoin(managers)
        manager_join = people.join(managers).outerjoin(boss)
        person_with_polymorphic = (
            [Person, Manager, Engineer], person_join)
        manager_with_polymorphic = ('*', manager_join)
        return person_with_polymorphic,\
            manager_with_polymorphic
