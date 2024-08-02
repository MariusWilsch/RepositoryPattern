import pytest, os, sys
from unittest.mock import MagicMock

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/base_repository")
from base_repository.base_repository import SupabaseSingleton, BaseRepository

@pytest.fixture
def mock_supabase():
    return MagicMock()


# class TestSupabaseSingleton:
#     pass

def test_save_user(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.save_user("test@test.com", "test")
    assert user["email"] == "test@test.com"
    assert user["password"] == "test"

def test_get_user(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.get_user("test@test.com")
    assert user["email"] == "test@test.com"

def test_update_user(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.update_user("test@test.com", "test")
    assert user["email"] == "test@test.com"
    assert user["password"] == "test"


def test_get_user_by_email(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.get_user_by_email("test@test.com")
    assert user["email"] == "test@test.com"

def test_update_user_by_email(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.update_user_by_email("test@test.com", "test")
    assert user["email"] == "test@test.com"


def test_get_user_by_id(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.get_user_by_id("test@test.com")
    assert user["email"] == "test@test.com"

def test_update_user_by_id(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.update_user_by_id("test@test.com", "test")
    assert user["email"] == "test@test.com"


def test_delete_user(mock_supabase):
    supabase = SupabaseSingleton(mock_supabase)
    user = supabase.delete_user("test@test.com")
    assert user["email"] == "test@test.com"

if __name__ == "__main__":
    pytest.main()