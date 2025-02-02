"""Tests for get_dates function."""

def test_get_dates_empty():
    """Test get_dates with empty data."""
    import A_GIS.Dev.Metrics.get_dates
    
    data = {}
    dates = A_GIS.Dev.Metrics.get_dates(data=data)
    assert dates == []


def test_get_dates_single():
    """Test get_dates with a single issue."""
    import A_GIS.Dev.Metrics.get_dates
    import datetime
    
    data = {
        "1": {
            "closed_at": "2024-01-01T12:00:00Z",
            "labels": []
        }
    }
    dates = A_GIS.Dev.Metrics.get_dates(data=data)
    assert len(dates) == 1
    assert isinstance(dates[0], datetime.datetime)
    assert dates[0].year == 2024
    assert dates[0].month == 1
    assert dates[0].day == 1


def test_get_dates_multiple():
    """Test get_dates with multiple issues."""
    import A_GIS.Dev.Metrics.get_dates
    
    data = {
        "1": {
            "closed_at": "2024-01-01T12:00:00Z",
            "labels": []
        },
        "2": {
            "closed_at": "2024-01-02T12:00:00Z",
            "labels": []
        },
        "3": {
            "closed_at": "2024-01-01T13:00:00Z",
            "labels": []
        }
    }
    dates = A_GIS.Dev.Metrics.get_dates(data=data)
    assert len(dates) == 3
    # Check sorting
    assert dates[0] < dates[1] < dates[2]


def test_get_dates_by_key():
    """Test get_dates with different keys."""
    import A_GIS.Dev.Metrics.get_dates
    
    data = {
        "1": {
            "closed_at": "2024-01-01T12:00:00Z",
            "started_at": "2024-01-01T10:00:00Z",
            "labels": []
        }
    }
    closed_dates = A_GIS.Dev.Metrics.get_dates(data=data, key="closed_at")
    started_dates = A_GIS.Dev.Metrics.get_dates(data=data, key="started_at")
    assert closed_dates[0].hour == 12
    assert started_dates[0].hour == 10


def test_get_dates_missing_key():
    """Test get_dates with missing keys."""
    import A_GIS.Dev.Metrics.get_dates
    
    data = {
        "1": {
            "closed_at": "2024-01-01T12:00:00Z",
            "labels": []
        },
        "2": {
            "labels": []  # No closed_at
        }
    }
    dates = A_GIS.Dev.Metrics.get_dates(data=data)
    assert len(dates) == 1  # Only one date should be found


def test_get_dates_by_label():
    """Test get_dates with label filtering."""
    import A_GIS.Dev.Metrics.get_dates
    
    data = {
        "1": {
            "closed_at": "2024-01-01T12:00:00Z",
            "labels": ["bug"]
        },
        "2": {
            "closed_at": "2024-01-02T12:00:00Z",
            "labels": ["feature"]
        },
        "3": {
            "closed_at": "2024-01-03T12:00:00Z",
            "labels": ["bug", "critical"]
        }
    }
    bug_dates = A_GIS.Dev.Metrics.get_dates(data=data, label="bug")
    feature_dates = A_GIS.Dev.Metrics.get_dates(data=data, label="feature")
    assert len(bug_dates) == 2
    assert len(feature_dates) == 1
    assert bug_dates[0].day == 1
    assert bug_dates[1].day == 3
    assert feature_dates[0].day == 2


def test_get_dates_unique():
    """Test get_dates with unique flag."""
    import A_GIS.Dev.Metrics.get_dates
    
    data = {
        "1": {
            "closed_at": "2024-01-01T12:00:00Z",
            "labels": []
        },
        "2": {
            "closed_at": "2024-01-01T12:00:00Z",  # Same exact time
            "labels": []
        },
        "3": {
            "closed_at": "2024-01-02T12:00:00Z",
            "labels": []
        }
    }
    # Without unique flag
    dates = A_GIS.Dev.Metrics.get_dates(data=data, unique=False)
    assert len(dates) == 3  # Should have all dates
    
    # With unique flag
    unique_dates = A_GIS.Dev.Metrics.get_dates(data=data, unique=True)
    assert len(unique_dates) == 2  # Should only have unique dates


def test_get_dates_unique_with_labels():
    """Test get_dates with unique flag and label filtering."""
    import A_GIS.Dev.Metrics.get_dates
    
    data = {
        "1": {
            "closed_at": "2024-01-01T12:00:00Z",
            "labels": ["bug"]
        },
        "2": {
            "closed_at": "2024-01-01T12:00:00Z",  # Same time
            "labels": ["bug"]
        },
        "3": {
            "closed_at": "2024-01-01T12:00:00Z",  # Same time
            "labels": ["feature"]  # Different label
        }
    }
    # With unique flag and bug label
    unique_bug_dates = A_GIS.Dev.Metrics.get_dates(
        data=data, 
        label="bug", 
        unique=True
    )
    assert len(unique_bug_dates) == 1  # Should only have one unique date for bugs 