import sqlalchemy as sa
from sqlalchemy_utils import sort_query
from tests import TestCase


class TestSortQuery(TestCase):
    def test_without_sort_param_returns_the_query_object_untouched(self):
        query = self.session.query(self.Article)
        sorted_query = sort_query(query, '')
        assert query == sorted_query

    def test_sort_by_column_ascending(self):
        query = sort_query(self.session.query(self.Article), 'name')
        assert 'ORDER BY article.name ASC' in str(query)

    def test_sort_by_column_descending(self):
        query = sort_query(self.session.query(self.Article), '-name')
        assert 'ORDER BY article.name DESC' in str(query)

    def test_skips_unknown_columns(self):
        query = self.session.query(self.Article)
        sorted_query = sort_query(query, '-unknown')
        assert query == sorted_query

    def test_sort_by_calculated_value_ascending(self):
        query = self.session.query(
            self.Category, sa.func.count(self.Article.id).label('articles')
        )
        query = sort_query(query, 'articles')
        assert 'ORDER BY articles ASC' in str(query)

    def test_sort_by_calculated_value_descending(self):
        query = self.session.query(
            self.Category, sa.func.count(self.Article.id).label('articles')
        )
        query = sort_query(query, '-articles')
        assert 'ORDER BY articles DESC' in str(query)

    def test_sort_by_subqueried_scalar(self):
        article_count = (
            sa.sql.select(
                [sa.func.count(self.Article.id)],
                from_obj=[self.Article.__table__]
            )
            .where(self.Article.category_id == self.Category.id)
            .correlate(self.Category.__table__)
        )

        query = self.session.query(
            self.Category, article_count.label('articles')
        )
        query = sort_query(query, '-articles')
        assert 'ORDER BY articles DESC' in str(query)

    def test_sort_by_aliased_joined_entity(self):
        alias = sa.orm.aliased(self.Category, name='categories')
        query = self.session.query(
            self.Article
        ).join(
            alias, self.Article.category
        )
        query = sort_query(query, '-categories-name')
        assert 'ORDER BY categories.name DESC' in str(query)

    def test_sort_by_joined_table_column(self):
        query = self.session.query(self.Article).join(self.Article.category)
        sorted_query = sort_query(query, 'category-name')
        assert 'category.name ASC' in str(sorted_query)

    def test_sort_by_multiple_columns(self):
        query = self.session.query(self.Article)
        sorted_query = sort_query(query, 'name', 'id')
        assert 'article.name ASC, article.id ASC' in str(sorted_query)

    def test_sort_by_column_property(self):
        self.Category.article_count = sa.orm.column_property(
            sa.select([sa.func.count(self.Article.id)])
            .where(self.Article.category_id == self.Category.id)
            .label('article_count')
        )

        query = self.session.query(self.Category)
        sorted_query = sort_query(query, 'article_count')
        assert 'article_count ASC' in str(sorted_query)
