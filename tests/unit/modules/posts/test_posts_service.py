import pytest

from minumtium.modules.posts import PostRepository, PostNotFoundException, PostService


def test_get_page_count(service: PostService):
    assert service.get_page_count(page_size=5) == 2


@pytest.mark.parametrize('page, expected_ids', ((0, ['0', '1']),
                                                (1, ['2', '3']),
                                                (2, ['4', '5'])))
def test_get_posts_for_page(page, expected_ids, service: PostService):
    first_post, second_post = service.get_posts_for_page(page=page, count=2)
    assert first_post.id == expected_ids[0]
    assert second_post.id == expected_ids[1]


def test_get_latest_posts_summary(service: PostService):
    first, second = service.get_latest_posts_summary(count=2)
    assert first.id == '0'
    assert second.id == '1'


def test_get_post(service):
    post = service.get_post(post_id='0')
    assert post.id == '0'
    assert post.title == 'This is the first post'
    assert post.author == 'danodic'
    assert post.body == 'This is a sample post.'


def test_add_post(service):
    id = service.add_post('Sample Post', 'Sample Body', 'Sample Author')
    assert id == '0'


def test_get_post_invalid_id(service):
    with pytest.raises(PostNotFoundException):
        service.get_post(post_id='invalid')


def test_get_latest_post(service):
    post = service.get_latest_post()
    assert post.id == '0'
    assert post.title == 'This is the first post'
    assert post.author == 'danodic'
    assert post.body == 'This is a sample post.'


@pytest.fixture()
def service(posts_database_adapter) -> PostService:
    repo = PostRepository(posts_database_adapter)
    return PostService(repo)
