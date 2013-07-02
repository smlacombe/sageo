import sqlalchemy as sa
from sqlalchemy_utils import merge

from tests import TestCase


class TestMerge(TestCase):
    def create_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))

            def __repr__(self):
                return 'User(%r)' % self.name

        class BlogPost(self.Base):
            __tablename__ = 'blog_post'
            id = sa.Column(sa.Integer, primary_key=True)
            title = sa.Column(sa.Unicode(255))
            content = sa.Column(sa.UnicodeText)
            author_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))

            author = sa.orm.relationship(User)

        self.User = User
        self.BlogPost = BlogPost

    def test_updates_foreign_keys(self):
        john = self.User(name=u'John')
        jack = self.User(name=u'Jack')
        post = self.BlogPost(title=u'Some title', author=john)
        post2 = self.BlogPost(title=u'Other title', author=jack)
        self.session.add(john)
        self.session.add(jack)
        self.session.add(post)
        self.session.add(post2)
        self.session.commit()
        merge(john, jack)
        assert post.author == jack
        assert post2.author == jack

    def test_deletes_from_entity(self):
        john = self.User(name=u'John')
        jack = self.User(name=u'Jack')
        self.session.add(john)
        self.session.add(jack)
        self.session.commit()
        merge(john, jack)
        assert john in self.session.deleted


class TestMergeManyToManyAssociations(TestCase):
    def create_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))

            def __repr__(self):
                return 'User(%r)' % self.name

        team_member = sa.Table(
            'team_member', self.Base.metadata,
            sa.Column(
                'user_id', sa.Integer,
                sa.ForeignKey('user.id', ondelete='CASCADE'),
                primary_key=True
            ),
            sa.Column(
                'team_id', sa.Integer,
                sa.ForeignKey('team.id', ondelete='CASCADE'),
                primary_key=True
            )
        )

        class Team(self.Base):
            __tablename__ = 'team'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))

            members = sa.orm.relationship(
                User,
                secondary=team_member,
                backref='teams'
            )

        self.User = User
        self.Team = Team

    def test_when_association_only_exists_in_from_entity(self):
        john = self.User(name=u'John')
        jack = self.User(name=u'Jack')
        team = self.Team(name=u'Team')
        team.members.append(john)
        self.session.add(john)
        self.session.add(jack)
        self.session.commit()
        merge(john, jack)
        assert john not in team.members
        assert jack in team.members

    # def test_when_association_exists_in_both(self):
    #     john = self.User(name=u'John')
    #     jack = self.User(name=u'Jack')
    #     team = self.Team(name=u'Team')
    #     team.members.append(john)
    #     team.members.append(jack)
    #     self.session.add(john)
    #     self.session.add(jack)
    #     self.session.commit()
    #     merge(john, jack)
    #     assert john not in team.members
    #     assert jack in team.members
    #     count = self.session.execute(
    #         'SELECT COUNT(1) FROM team_member'
    #     ).fetchone()[0]
    #     assert count == 1


class TestMergeManyToManyAssociationObjects(TestCase):
    def create_models(self):
        class Team(self.Base):
            __tablename__ = 'team'
            id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
            name = sa.Column(sa.Unicode(255))

        class User(self.Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
            name = sa.Column(sa.Unicode(255))

        class TeamMember(self.Base):
            __tablename__ = 'team_member'
            user_id = sa.Column(
                sa.Integer,
                sa.ForeignKey(User.id, ondelete='CASCADE'),
                primary_key=True
            )
            team_id = sa.Column(
                sa.Integer,
                sa.ForeignKey(Team.id, ondelete='CASCADE'),
                primary_key=True
            )
            role = sa.Column(sa.Unicode(255))
            team = sa.orm.relationship(
                Team,
                backref=sa.orm.backref(
                    'members',
                    cascade='all, delete-orphan'
                ),
                primaryjoin=team_id == Team.id,
            )
            user = sa.orm.relationship(
                User,
                backref=sa.orm.backref(
                    'memberships',
                    cascade='all, delete-orphan'
                ),
                primaryjoin=user_id == User.id,
            )

        self.User = User
        self.TeamMember = TeamMember
        self.Team = Team

    def test_when_association_only_exists_in_from_entity(self):
        john = self.User(name=u'John')
        jack = self.User(name=u'Jack')
        team = self.Team(name=u'Team')
        team.members.append(self.TeamMember(user=john))
        self.session.add(john)
        self.session.add(jack)
        self.session.add(team)
        self.session.commit()
        merge(john, jack)
        self.session.commit()
        users = [member.user for member in team.members]
        assert john not in users
        assert jack in users

    # def test_when_association_exists_in_both(self):
    #     john = self.User(name=u'John')
    #     jack = self.User(name=u'Jack')
    #     team = self.Team(name=u'Team')
    #     team.members.append(self.TeamMember(user=john))
    #     team.members.append(self.TeamMember(user=jack))
    #     self.session.add(john)
    #     self.session.add(jack)
    #     self.session.add(team)
    #     self.session.commit()
    #     merge(john, jack)
    #     users = [member.user for member in team.members]
    #     assert john not in users
    #     assert jack in users
    #     assert self.session.query(self.TeamMember).count() == 1
