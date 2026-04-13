def test_version_exists():
    import semantic_search
    assert hasattr(semantic_search, '__version__')
