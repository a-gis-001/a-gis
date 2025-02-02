def test_basic_filters():
    """Test the filter_issues function with various scenarios.

    Tests:
        1. Filtering by label
        2. Filtering by closed status
        3. Filtering by both label and closed status
        4. Edge cases (empty data, None values)
    """
    import A_GIS.Dev.Metrics.filter_issues

    # Test data
    test_data = {
        1: {
            "labels": ["bug", "critical"],
            "closed_at": "2024-01-01T00:00:00Z",
        },
        2: {
            "labels": ["feature"],
            "closed_at": None,
        },
        3: {
            "labels": ["bug"],
            "closed_at": "2024-01-02T00:00:00Z",
        },
        4: {
            "labels": [],
            "closed_at": None,
        }
    }

    # Test 1: Filter by label 'bug'
    filtered = A_GIS.Dev.Metrics.filter_issues(
        data=test_data,
        label="bug",
        closed_only=False
    )
    assert len(filtered) == 2
    assert 1 in filtered
    assert 3 in filtered

    # Test 2: Filter closed only
    filtered = A_GIS.Dev.Metrics.filter_issues(
        data=test_data,
        label=None,
        closed_only=True
    )
    assert len(filtered) == 2
    assert 1 in filtered
    assert 3 in filtered

    # Test 3: Filter by label 'bug' and closed only
    filtered = A_GIS.Dev.Metrics.filter_issues(
        data=test_data,
        label="bug",
        closed_only=True
    )
    assert len(filtered) == 2
    assert 1 in filtered
    assert 3 in filtered

    # Test 4: Filter by non-existent label
    filtered = A_GIS.Dev.Metrics.filter_issues(
        data=test_data,
        label="nonexistent",
        closed_only=False
    )
    assert len(filtered) == 0

    # Test 5: Empty data
    filtered = A_GIS.Dev.Metrics.filter_issues(
        data={},
        label="bug",
        closed_only=False
    )
    assert len(filtered) == 0

    # Test 6: No filters (should return original data)
    filtered = A_GIS.Dev.Metrics.filter_issues(
        data=test_data,
        label=None,
        closed_only=False
    )
    assert len(filtered) == len(test_data)
    assert filtered == test_data

    # Test 7: Missing labels field
    test_data_missing_labels = {
        1: {
            "closed_at": "2024-01-01T00:00:00Z"
        }
    }
    filtered = A_GIS.Dev.Metrics.filter_issues(
        data=test_data_missing_labels,
        label="bug",
        closed_only=False
    )
    assert len(filtered) == 0

    print("All tests passed!")
