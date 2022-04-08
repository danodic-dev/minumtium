from datetime import datetime

import pytest

from minumtium.modules.posts import Post, PostRepository, PostNotFoundException

sample_post = Post(
    title='This is a sample post.',
    author='danodic',
    body='This is a sample post.',
    timestamp=datetime(2022, 2, 22, 22, 22, 22, 222222))

another_post = Post(
    title='This is another post.',
    author='beutrano',
    body='A different body.',
    timestamp=datetime(2023, 3, 23, 23, 23, 23, 222222))


def test_save(repo: PostRepository):
    inserted_id = repo.save(sample_post)
    assert isinstance(inserted_id, str)
    assert inserted_id == '0'


def test_get(repo: PostRepository):
    post = repo.get('0')
    assert isinstance(post, Post)
    assert post.author == 'danodic'
    assert post.body == 'This is a sample post.'
    assert post.title == 'This is the first post'


def test_get_post_invalid_id(repo: PostRepository):
    with pytest.raises(PostNotFoundException):
        repo.get('invalid')


def test_get_all_posts(repo: PostRepository):
    posts = repo.get_all()
    first_post, second_post = posts[:2]

    assert isinstance(first_post, Post)
    assert first_post.author == 'danodic'
    assert first_post.body == 'This is a sample post.'
    assert first_post.title == 'This is the first post'

    assert isinstance(second_post, Post)
    assert second_post.author == 'beutrano'
    assert second_post.body == 'This is a sample post.'
    assert second_post.title == 'This is the second post'


def test_summary(repo: PostRepository):
    first, second, third, fourth, fifth = repo.get_summary(count=5)

    assert isinstance(first, Post)
    assert first.title == 'This is the first post'
    assert 'body' not in first

    assert isinstance(second, Post)
    assert second.title == 'This is the second post'
    assert 'body' not in first

    assert isinstance(third, Post)
    assert third.title == 'This is the third post'
    assert 'body' not in first

    assert isinstance(fourth, Post)
    assert fourth.title == 'This is the fourth post'
    assert 'body' not in first

    assert isinstance(fifth, Post)
    assert fifth.title == 'This is the fifth post'
    assert 'body' not in first


@pytest.fixture()
def repo(posts_database_adapter) -> PostRepository:
    return PostRepository(posts_database_adapter)
